#!/usr/bin/python

# exec_imap.py

#### Written by:
#        Erika Burdon
#        Software Engineering Student
#        University of Victoria             British Columbia, CANADA
#        https://github.com/eburdon
#         eburdonGIT@gmail.com
#        All comments and critques on this script are welcome!
#
#		LinkedIn:	/in/eburdon
#		Riipen:		/users/1017
########

# Connects to GMail and parses Transparent Language emails with IMAP
# NOTE: SEE README FOR SPECIAL NOTE ABOUT THIS SCRIPT DELETING MESSAGES

import imaplib      # IMAP stuff... obviously
import email        # Unpacking MIME messages

# Import MY modules
import myGlobals
from common import *


def executeIMAP():
    newMsgFlag = 0
    funnyCharFlag = 0
    
    # Parsing Vars
    vFlag = False
    exStart = 0        # Example sentence start (Ger)
    exEnd = 0        # Example sentence end
    prefix = '=?UTF-8?B?'        # Start of base-64 ecoding
    suffix = '?='                # End of encoding

    # Initalizers
    delList = []
    newWord = []
    
    # --- Connect to a server & login
    server = imaplib.IMAP4_SSL(myGlobals.host)
    #try:
    server.login(myGlobals.usrnm, myGlobals.usrpss)
    #except e:
    #    print "Could not log into gmail!"
    #    print e

    ## List GMail FOLDERS (*not* tabs/boxes) [e.g., filter]
    ## mailboxes = server.list()
    ## print mailboxes
    
    # --- Connect to inbox (Or other mailbox folder...)
    try:
        server.select("INBOX")
    except e:
        print "Could not select INBOX"
        print e
    
    # --- Get ALL email and their Unique IDentifiers (UID)
    result, data = server.uid('search', None, 'All')

    # --- Data is a list of UIDs; Tidy up
    UIDs = data[0]
    UIDs_list = UIDs.split()
    
    for email_ID in UIDs_list:
        # -- Get email's header & msg content (RFC822 == ALL)
        result, data = server.uid('fetch', email_ID, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        subj = email_message['Subject']
        
        # NOTE: Some vocabulary words have umlauts, and the 
        #    resulting subject is base-64 encoded (the useful
        #    content is between '=?UTF=8?B?' and '?=')
        #     Thus, this needs to be extracted then decoded
        if prefix in subj:
            funnyCharFlag = 1
            # Extract data part of the string
            useful = subj[len(prefix):len(subj)-len(suffix)]
            # Decode the bytes
            decoded = base64.b64decode(useful)
            # Decode the utf-8
            decoded = unicode(decoded, "utf8")
            # Set new/readable subject
            subj = decoded

        # -- Check email's subject; See if its a desired vocab msg
        if 'German Word of the Day' in subj:
        
            # - Init write-to-file elements 
            wod = ["Word: "]
            meaning = ["Means: "]
            prtspch = ["Part", "of", "speech:"]
            exSentence  = ["Example", "sentence:"]
            exTrSentence = ["This", "means:"]
            
            # - Notify user they have new vocab asap
            if newMsgFlag == 0:
                print "\nYou have new vocabulary!"
                newMsgFlag += 1

            # - Append THIS EMAIL's ID to potential delete list
            delList.append(email_ID)
            
            # - Process/Get payload
            # email_message = email.message_from_string(raw_email)
            parsed_full_msg = get_payload(email_message)
            
            # -- Begin parsing --
            
            # Get part of speech (verb, adjective, etc...)
            get_part_speech(vFlag, prtspch, parsed_full_msg)
            
            # Get word (German) & meaning (english)
            get_DE_word(vFlag, newWord, wod, meaning, 
                                                parsed_full_msg)

            # Get example/word in context of a sentence; 
            exEnd = get_DE_example(parsed_full_msg, exStart, 
                                            exEnd, exSentence)

            # Get translation of example sentence
            get_EN_example(parsed_full_msg, exEnd, exTrSentence)
            
            # -- End parsing --
            
            # - Open file for appending; pointer will be @ end 
            # of the file. If file does not exist, it will be 
            # created
            fp = open(myGlobals.saveToFile, "a")
            
            ## --------- Add each entry to file ----------
            add_element(fp, wod)
            add_element(fp, meaning)
            add_element(fp, prtspch)
            add_element(fp, exSentence)
            add_element(fp, exTrSentence)
                    
            # --- End of entry indicator/separator
            fp.write("---------------------------\n")
                
            # Flushes any unwritten information and closes fileobj
            fp.close()
            

    # --- Console messages/User information
    # Confirm new entries
    if newMsgFlag == 0:
        print "\nYou have no new vocab!"
        exit_program(server, 0)

    # List new entries
    print "\nThe following words have been added to your vocab",
    print "file:"
    
    if funnyCharFlag == 1:
        print ""
        print "[ Note: Some characters (such as umlauts) may be", 
        print "unreadable on your console. They have, however,", 
        print "been correctly copied into your file. ]"
    print ""
    
    for word in newWord:
        print word
    print ""
    

    # --- Delete original email messages from INBOX
    confirm = confirm_yes_no("Would you like to delete these emails from your Google Inbox?", "no")
    
    if confirm == True:
        print "Processing..."
        for num in delList:
            mov, data = server.uid('STORE', num, '+FLAGS', '(\Deleted)')
            
        # -- Push all changes
        try:
            server.expunge() # When testing, remember to F5 site
            print len(delList), "Messages deleted."
        except:
            print "The server could not delete any messages."
           # exit_program(server, 1)
    else:
        print "No action taken."


    # --- Close program without errors
    # exit_program(server, 0)
    
