#!/usr/bin/python

# exec_POP.py

#### Written by:
#        Erika Burdon
#        Software Engineering Student
#        University of Victoria             British Columbia, CANADA
#        https://github.com/eburdon
#        eburdonGIT@gmail.com
#        All comments and critques on this script are welcome!
#
#		website:	web.uvic.ca/~eburdon
#		LinkedIn:	/in/eburdon
#		Riipen:		/users/1017
########

# Connects to GMail and parses Transparent Language emails with POP3

import poplib    	# Getting emails
import email 		# unpacking MIME messages
from email import parser, FeedParser
from optparse import OptionParser

# Import MY modules
import myGlobals
from common import *

def executePOP():
    # Connect to server
    host = 'pop.gmail.com'
    pop_conn = poplib.POP3_SSL(myGlobals.host)
    # print pop_conn.getwelcome()
    
    pop_conn.user(myGlobals.usrnm)
    pop_conn.pass_(myGlobals.usrpss)
	
    # Get ALL messages from server
    messages = [pop_conn.retr(i) for i in range (1, len(pop_conn.list()[1]) + 1)]
    messages = ["\n".join(mssg[1]) for mssg in messages]
    # Parse message from email object
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]

	# SET UP DATA ARRAYS
    matches = []  # Messages with 'German Word of Day' subject
    delList = []  # Lists index vals of vocab emails for later del
    newWord = []  # Array of all new german words (confirmation)

    # Get emails with new vocabulary words; Construct 'matches'
    get_vocab_messages(messages, matches, delList)
    
    # Decide if program will continue (are there new vocab words?)
    get_status_new_vocab(pop_conn, matches)
    
    # I can now iterate through 'matches' and get body messages
    for curr in matches:
        for part in curr.walk():
    
            # Multipart is just a container; Skip
            if part.get_content_maintype() == 'multipart':
                continue

            if part.get_content_maintype() == 'text':
                # Email HTML formating; Each msg has one. SKIP
                if part.get_content_type() == 'text/hmtl':
                    continue;
        
                # Actual content I want to parse
                if part.get_content_type() == 'text/plain':
                
                    # Message is NOT a multipart; Payload 
                    #     returns a string of words (not list)
                    fullMsg=part.get_payload(decode=True).split()
                    
                    
                    # ----- Initalize write to file elements -----
                    wod = ["Word: "]             #Of the day
                    meaning = ["Means: "]
                    prtspch = ["Part", "of", "speech:"]
                    exSentence = ["Example", "sentence:"]
                    exTrSentence = ["This", "means:"]
                    
                    # --------------- Parsing vars ---------------
                    vFlag = False    # Is word a verb?
                    exStart = 0        # Example sentence start (Ger)
                    exEnd = 0        # Example sentence end 
                
                
                    ## --------------- Parse email ---------------
                    
                    # Get part of speech (verb, adjective, etc...)
                    get_part_speech(vFlag, prtspch, fullMsg)
                    
                    # Get word (German) & meaning (english)
                    get_DE_word(vFlag, 
                                newWord, wod, meaning, fullMsg)
                    
                    # Get example/word in context of a sentence; 
                    # Returns end of example so translations knows
                    # where to start.
                    exEnd = get_DE_example(fullMsg, exStart,
                                            exEnd, exSentence)
                    
                    # Get translation of example sentence
                    get_EN_example(fullMsg, exEnd, exTrSentence)
                    
                    ## --------- Add each entry to file ----------
                
                    # Opens the file for appending; pointer will 
                    #    be at the end of the file
                    #     If file does not exist, it will be created
                    fp = open(myGlobals.saveToFile, "a")
                    
                    add_element(fp, wod)
                    add_element(fp, meaning)
                    add_element(fp, prtspch)
                    add_element(fp, exSentence)
                    add_element(fp, exTrSentence)
                    
                    # End of entry
                    fp.write("---------------------------\n")
                
                    # Flushes any unwritten information and 
                    #    closes file object; Good practice to 
                    #    include
                    fp.close()
    ## ----------------------------------------------------------
    
    # Before closing connection, I want to delete the emails 
    #    (The purpose of this script is to de-clutter my inbox)
    #     But! I want user confirmation -- they may want to read 
    #     the original message to, e.g., listen to the audio clip.
    ##    Note: POP3 does not support marking email as 'read'; 
    ##       They are simply 'seen' by the python perspective/user
    ##    Note: Users can find all deleted emails in 'Trash'
    
	if (len(newWord) !=0 ):
		confirm_new(newWord)

		delAction = confirm_yes_no("Are you sure you want to delete their original messages from your Google inbox?\n", "no")

		if delAction == False:
			print "\nNo emails deleted.\n"
		elif delAction == True:
			delete_vocab_emails(pop_conn, delList)
		else:
			print "\nSystem error!\n"
			sys.exit(1)
	pop_conn.quit()