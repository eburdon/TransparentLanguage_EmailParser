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
#		website:	web.uvic.ca/~eburdon
#		LinkedIn:	/in/eburdon
#		Riipen:		/users/1017
########

# Connects to GMail and parses Transparent Language emails with IMAP
# NOTE: SEE README FOR SPECIAL NOTE ABOUT THIS SCRIPT DELETING MESSAGES

import 	imaplib      # IMAP stuff... obviously
import 	email        # Unpacking MIME messages
import wx

# Import MY modules
import 	myGlobals
from 	common 	 import *

def newMessages():
	wx.MessageBox('You have new messages!', 'Alert!', wx.OK)

def noNewMessages():
	wx.MessageBox('You have no new messages!', 'Alert!', wx.OK)

# Checks vocab word (included in subject line) for special characters such as umlauts - the need special handling for correct processing into vocabulary file
def check_specialCharacters(subject, flag):
    prefix 	= '=?UTF-8?B?'        # Start of base-64 ecoding
    suffix 	= '?='                # End of encoding
    if prefix in subject:
            flag = 1        # Set global
            # Extract data part of the string
            useful 	= subject[len(prefix):len(subject)-len(suffix)]
            # Decode the bytes
            decoded = base64.b64decode(useful)
            # Decode the utf-8
            decoded = unicode(decoded, "utf8")
            # Set new/readable subject
            subject 	= decoded
    # Return same or updated subject
    return subject

def executeIMAP(self):
    # --- Flag Variables (0 = false; 1 = true)
    newMsgFlag 		= 0
    funnyCharFlag 	= 0
    
    # -- Parsing Vars
    vFlag 	= False
    exStart = 0        # Example sentence start (Ger)
    exEnd 	= 0        # Example sentence end

    # --- Initalizers
    delList = []
    newWord = []
    
    # --- Connect to a server & login
    server = imaplib.IMAP4_SSL(myGlobals.host)
    server.login(myGlobals.usrnm, myGlobals.usrpss)
    
    # --- Connect to INBOX
    try:
        server.select("INBOX")
    except e:
        print "Could not select INBOX"
        print e
    
    
    # --- Get ALL email and their Unique IDentifiers (UID)
    result, data = server.uid('search', None, 'All')

    # --- Data is a list of UIDs; Tidy up
    UIDs 		= data[0]
    UIDs_list 	= UIDs.split()
    
	
	###                                             ###
	# BEGIN COLLECTING EMAILS AND ITERATING THROUGH   #
	###                                             ###
    for email_ID in UIDs_list:
    
        # -- Get email's header & msg content (RFC822 == ALL)
        result, data 	= server.uid('fetch', email_ID, '(RFC822)')
        raw_email 		= data[0][1]
        email_message 	= email.message_from_string(raw_email) 
        subj 			= email_message['Subject'] 

        
        # Inspects current subject line for odd characters (e.g., umlauts)
        #   and decodes them so they may be read by my parser
        #! print "sub1:", subj 
        subj = check_specialCharacters(subj, funnyCharFlag)
        #! print "subject2", subj
        
        
        # -- Check email's subject; See if its a desired vocab msg
        if 'German Word of the Day' in subj:
            
			# - Init write-to-file elements 
            wod          = ["Word: "]
            meaning      = ["Means: "]
            prtspch      = ["Part", "of", "speech:"]
            exSentence   = ["Example", "sentence:"]
            exTrSentence = ["This", "means:"] 
            
            # - Notify user they have new vocab A.S.A.P. (once)
            if newMsgFlag == 0:
                newMsgFlag = 1
                newMessages()

            # - Append THIS EMAIL's ID to potential DELETE list
            delList.append(email_ID)
            
            ## --- Process/Get payload ----------------- ##
            #! print "PROCESSING..."
            parsed_full_msg = get_payload(email_message)
            
            # -- Begin parsing ------------------------- ##
            
            # Get part of speech (verb, adjective, etc...)
            get_part_speech(vFlag, prtspch, parsed_full_msg)
            
            # Get word (German) & meaning (English)
            get_DE_word(vFlag, newWord, wod, meaning, 
                                                parsed_full_msg)

            # Get example/word in context of a sentence; 
            exEnd = get_DE_example(parsed_full_msg, exStart, 
                                            exEnd, exSentence)

            # Get translation of example sentence
            get_EN_example(parsed_full_msg, exEnd, exTrSentence)
            
            # -- End parsing ----------------------------- ##
            
            
            # -- File Handling --------------------------- ##
            
            # Open file for appending; file DNE? Be Created
            fp = open(myGlobals.saveToFile, "a")
            
            ## --------- Add each entry to file -------------
            add_element(fp, wod)
            add_element(fp, meaning)
            add_element(fp, prtspch)
            add_element(fp, exSentence)
            add_element(fp, exTrSentence)
                    
            # --- End of entry indicator / Entry separator --
            fp.write("---------------------------\n")
                
                
            # Flushes any unwritten information; closes file obj
            fp.close()
            
            # -- End File Handling ------------------------- ##
            
        #! print ""
    # -- end FOR loop -------------------------------------- ##

    #! print "\n\n --- FOR LOOP ENDED --- \n\n"
    
    
    ###           ###
    #   RESULTS     #
    ###           ###
	
    # --- Confirm new entries -------------------------- ##
    if newMsgFlag == 0:
        #! print "--DEBUG: I couldn't find any new vocab";
        noNewMessages()
        # I need to somehow escape this parser?
	    # exit(1)
    else:
        # New vocab has been added!

        # I WANT TO GET THIS INTO A MESSAGE BOX!
        # List new entries
        # print "\nThe following words have been added to your vocab",
        # print "file:"
    
        #if funnyCharFlag == 1:
        #print ""
        #print "[ Note: Some characters (such as umlauts) may be", 
        #print "unreadable on your console. They have, however,", 
        #print "been correctly copied into your file. ]"
        #print ""
	
        #for word in newWord:
        #   print word
        #	print ""
        
        
        ### -- CURRENT TASK: BUILDING A SCROLLING BOX #########
        scrollDisplayBox = wx.TextCtrl(self, wx.ID_ANY, style = wx.TE_MULTILINE, pos = (25,80), size = (200,100) )
        addOneString = ""
        lineCount = 0
        
        scrollDisplayBox.SetInsertionPointEnd()
        
        for word in newWord:
            addOneString = addOneString + word + "\n"
            lineCount = lineCount + 1
        scrollDisplayBox.AppendText(addOneString)
        
        # scrollDisplayBox.ScrollLines(-1)  ## Doesn't do anything?
        # scrollDisplayBox.Refresh()        ## Doesn't seem to do anything
        
        scrollDisplayBox.SetInsertionPointEnd()
        
        
        ## -- Program End ---------------------- ##
        print "EXIT THE PROGRAM - here I'll ask if you want to delete\n\n"
        # exit(1)
	
	
    # --- Delete original email messages from INBOX ------------------------------------------------------
    # confirm = confirm_yes_no("Would you like to delete these emails from your Google Inbox?", "no")
    
    # if confirm == True:
    #   print "Processing..."
    #    for num in delList:
    #        mov, data = server.uid('STORE', num, '+FLAGS', '(\Deleted)')
            
        # -- Push all changes
    #    try:
    #        server.expunge() # When testing, remember to F5 site
    #        print len(delList), "Messages deleted."
    #    except:
    #        print "The server could not delete any messages."
           # exit_program(server, 1)
    #else:
    #    print "No action taken."

class MyCustomWindow(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetSize((100,100))