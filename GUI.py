#!/usr/bin/python

# GUI.py

#### Written by:
#        Erika Burdon
#        Software Engineering Student
#        University of Victoria             British Columbia, CANADA
#        https://github.com/eburdon
#         eburdongit@gmail.com
#        All comments and critques on this script are welcome!
########

import myGlobals
from exec_imap import executeIMAP
from exec_POP import executePOP


def main():
    # GET USER INPUT FOR THESE VARIABLES
    myGlobals.init_globals('LANAAAAAA@gmail.com', 
                           'WHAT?!', 
                           'imap.googlemail.com', 
                           'C:\----\WordOfDayVocab.txt')
    print "Executing IMAP connection..."
    executeIMAP()
    # print "Executing POP3 connection..."
    # executePOP()


if __name__ == "__main__": main()
    