#!/usr/bin/python
# coding: iso-8859-1

# Common.py ; Common functions module for IMAP and POP3 parsing implementation

#### Written by:
#        Erika Burdon
#        Software Engineering Student
#        University of Victoria             British Columbia, CANADA
#        https://github.com/eburdon
#         eburdongit@gmail.com
#        All comments and critques on this script are welcome!
########

# Functions that are used similarly between IMAP and POP3

# ------------------------- Imports ------------------------------
import mimetypes
import re        # Reg Expressions
import string    # Parsing message strings
import sys        # sys.exit
import base64    # For decoding base-64 subject lines
import codecs
import myGlobals # Defines host, usrnm, usrpss, etc...

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

from _codecs import decode
from email.header import decode_header



# Could this cause problems later? TODO: Test!
# Had to change default encoding from Ascii to utf8 so the IMAP script
#    could parse Umlauts in some 'Subject' message headers
reload(sys)
sys.setdefaultencoding('utf8')

# ------------------ Outsourced Functions ------------------------
# Ask user yes/no question via raw_input; return decisive action.
# This function is overkill for this script, but I wanted to it 
#     be complete so that I have it for future reference.
# Function modified from:
#    Recipe 577058: http://code.activestate.com/recipes/577058/
##    Note: 'default' is presumed answer if user hits 'enter' 
##        (e.g., by accident)
def confirm_yes_no(question, default="no"):
    valid = {"Y":True,  "y":True,  "Yes":True, "yes":True, 
             "N":False, "n":False, "No":False, "no":False}
    
    if default == None:
        prompt = "[y/n]"
    elif default == "yes" or default == "Yes":
        prompt = "[Y/n]"
    elif default == "no" or default == "No":
        prompt = "[y/N]"
    
    while True:
        print question + prompt
        choice = raw_input()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print "Please enter a valid response: Type 'y' or ", 
            print "'n' and press ENTER"

# Note that if you want to get text content (body) and the email
#    contains multiple payloads (plaintext/html), you must parse
#    each message separately. Use something like the following:
#    (taken from a stackoverflow post)
def get_payload(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload(decode=True).split()
            else:
                print part.get_content_maintype()
                # Do nothing... you're NOTHING TO ME
    elif maintype == 'text':
        return email_message_instance.get_payload()

## ------------------ Parsing Functions -------------------------
#    Various functions parsing the email's full payload, fullMsg
def get_DE_word(vFlag, newWord, wod, meaning, fullMsg):
    # Find the index POSITION of the word 'Day' (parse fullMsg)
    
    for item in [item for item, x in enumerate(fullMsg) if x == 'Day']:
        wodpos = item+1
        
        while(1):
            wodd = fullMsg[wodpos]
            
            if ':' in wodd:
                wodd = wodd.strip(':')
                wod.append(wodd)
                newWord.append(wodd)
                break;
            else:
                # Append found match
                wod.append(wodd)
                newWord.append(wodd)
                # Increase position; Look at next word (loop)
                wodpos += 1
        
        # Get english word (immediately following)
        derp = get_EN_meaning(vFlag, meaning, wodpos, fullMsg)
        if derp == False:
            break;


def get_EN_meaning(vFlag, meaning, wodpos, fullMsg):
    # Check if word is verb; Easier to understand later if 'to'
    # is in front
    if vFlag:
        meaning.append("to " + fullMsg[wodpos+2])
        return True
    else:
        while(1):
            # Ensure you reach the end of the english part
            if '-' is fullMsg[wodpos+2]:
                meaning.append(fullMsg[wodpos+1])
                break;
            else:
                # If not, append and carry on
                meaning.append(fullMsg[wodpos+1])
                wodpos+=1
        return False
        
        
def get_part_speech(vFlag, prtspch, fullMsg):
    # Get word's part of speech (& set flag)
    for item in [item for item, x in enumerate(fullMsg) if x == 'speech:']:
        prtspchh = fullMsg[item+1]
        if prtspchh == 'verb':
            vFlag = True
        prtspch.append(prtspchh)

        
def get_DE_example(fullMsg, exStart, exEnd, exSentence):
    for item in [item for item, x in enumerate(fullMsg) if x == 'sentence:']: # 'Example sentence:'
        exStart = item+1
        
    for item in [item for item, x in enumerate(fullMsg) if x == 'Sentence']: # 'Sentence meaning:'
        exEnd = item
        
    for word in range(exStart, exEnd):
        exSentence.append(fullMsg[word])
        
    return exEnd

        
def get_EN_example(fullMsg, exEnd, exTrSentence):
    for item in [item for item, x in enumerate(fullMsg) if x == 'Listen']: # 'Sentence meaning:'
        for word in range(exEnd+2, item):
            exTrSentence.append(fullMsg[word])

            
## ------------------- Add-to-file Functions ---------------------
def add_element(fp, element):
    for i in element:
        fp.write(i)
        fp.write(" ")
    fp.write("\n")
    
    
# ---------------------- Closing Actions -------------------------
def confirm_new(newWord):
    print "This script successfully added the following (new)", 
    print " words into your vocabulary:\n"
    for word in newWord:
        print word
    print ""

def exit_program(server, exit_message):
    print "Terminating script..."
    server.close()
    server.logout()
    if exit_message == 1:
        # Some error! (Tracing)
        sys.exit(1)
    else:
        # Clean Exit (No problems)
        sys.exit(0)


# ----------------- USED ONLY IN POP; NEED TO REDESIGN?! ----------
def debug_print_all_subjects(messages):
    ## DEBUG; What are ALL my messages (subjects)?
    print "\n\nDEBUG: Printing all message subjects"
    n = 1
    for message in messages:
        print n, message['subject']
        n += 1
    print "\n\n"

def debug_any_new_messages(pop_conn):
    ## DEBUG; Do I have *any* messages?
    if pop_conn.stat()[1] > 0:
        print "\nYou have new mail!\n"
    else:
        print "No new mail."
        sys.exit(1)

## ---------------------------------------------------------------

# Puts all messages into array re: reference and iteration;
def get_vocab_messages(messages, matches, delList):
    i = 0
    for message in messages:
        re_DEword = re.compile(r'German Word of the Day(.)*')
        match = re_DEword.search(message['subject'])
        if match:
            matches.append(message)
            delList.append(i)
        i += 1

def get_status_new_vocab(pop_conn, matches):
    if len(matches) > 0:
        print "\nYou have new vocabulary words!"
    else:
        print "\nNo new words. Terminating script."
        pop_conn.quit()
        sys.exit(0)
