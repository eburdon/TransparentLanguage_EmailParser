#!/usr/bin/python

#         globals.py
#### Written by:
#        Erika Burdon
#        Software Engineering Student
#        University of Victoria             British Columbia, CANADA
#        https://github.com/eburdon
#         eburdongit@gmail.com
#        All comments and critques on this script are welcome!
#
#		LinkedIn:	/in/eburdon
#		Riipen:		/users/1017
########

# ----------------------- Global Vars ----------------------------

def init_globals(USRNM, USRPSS, HOST, SAVETOFILE):
    # I may include some sort of set up where users can either save 
    #    and store their login information, or will have the script
    #    run automatically on click. Right now, it is the latter.
    global usrnm
    usrnm = USRNM
    global usrpss
    usrpss = USRPSS
    # Also including host here; Users may opt to change
    global host
    host = HOST
    # Save to file; User may also specify
    global saveToFile
    saveToFile = SAVETOFILE
