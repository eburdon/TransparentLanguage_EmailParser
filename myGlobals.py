#!/usr/bin/python

# myGlobals.py

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

# ----------------------- Global Vars ----------------------------
# SET DEFAULTS
usrnm = ""
usrpss = ""
host = "imap.googlemail.com"		# DEFAULT
saveToFile = "WordOfDayVocab.txt"		# DEFAULT
# ----------------------------------------------------------------

def init_globals(USRNM, USRPSS):
    global usrnm
    usrnm = USRNM
    global usrpss
    usrpss = USRPSS
    # global host
    # host = HOST
    # global saveToFile
    # saveToFile = SAVETOFILE
	
def set_username(USRNM):
	global usrnm
	usrnm = USRNM

def set_pwd(USRPSS):
	global usrpss
	usrpss = USRPSS
	
def set_host(HOST):
	global host
	host = HOST

def set_saveFile(SAVETOFILE):
	global saveToFile
	saveToFile = SAVETOFILE