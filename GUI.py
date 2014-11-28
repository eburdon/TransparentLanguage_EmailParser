#!/usr/bin/python

# GUI.py
#	User Interface for Transparent Language daily message
#	parsing

#### Written by:
#        Erika Burdon
#        Software Engineering Student
#        University of Victoria             BC, CANADA
#        https://github.com/eburdon
#        eburdongit@gmail.com
#        All comments and critques on this script are welcome!
#
#		Koding:		/karmaqueenn
#		LinkedIn:	erika-burdon/42/492/333
#		Riipen:		/users/1017
########

import myGlobals
from exec_imap import executeIMAP
from exec_POP import executePOP

import wx


class MyGUI(wx.Frame):
	# MENU FUNCTIONS
	def OnQuit(self, event):
		self.Close()

	
	# BUTTON FUNCTIONS
	def runIMAP(self, event):
		print "Run IMAP"
		
	def runPOP(self, event):
		print "Run POP3"
	
	
	# APPEARANCE FUNCTIONS
	def establishMenu(self):
		# CREATE a menu bar; Each has menu items which can be:
		#	normal, check, or radio items
		topmenubar = wx.MenuBar()
		
		# CREATE three primary (sub)menu ----------------------
		file = wx.Menu()	# 100
		edit = wx.Menu()	# 200
		help = wx.Menu()	# 300
		
		## FILE MENU ------------------------------------------
		# Append(ID, Link Name, Lower bar caption)
		file.Append(101, '&Open', 'Open a new document')
		file.Append(102, '&Save', 'Save the document')
		file.AppendSeparator()	# Separate with a horiz line
		quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
		file.AppendItem(quit)
		
		# Bind function to menu CLICK event
		self.Bind(wx.EVT_MENU, self.OnQuit, id=105)
		
		## EDIT MENU ------------------------------------------
		edit.Append(201, 'check item1', '', wx.ITEM_CHECK)
		edit.Append(202, 'check item2', kind=wx.ITEM_CHECK)
		
		## HELP MENU ------------------------------------------
		help.Append(301, 'Help item 1', 'Dosomething useful')
		
		# ADD SUBMENUS to MENU --------------------------------
		topmenubar.Append(file, '&File')
		topmenubar.Append(edit, '&Edit')
		topmenubar.Append(help, '&Help')
		
		# CONSTRUCT menubar in application --------------------
		self.SetMenuBar(topmenubar)
		
	def establishButtons(self):
		pnl = wx.Panel(self)
		
		imapButton = wx.Button(pnl, label='IMAP', pos=(20,30))
		imapButton.Bind(wx.EVT_BUTTON, self.runIMAP)
		
		popButton = wx.Button(pnl, label='POP3', pos=(50,60))
		popButton.Bind(wx.EVT_BUTTON, self.runPOP)
		
	# EXECUTING THE GUI
	def __init__(self, parent, id, title):
		# MAIN FRAME SET UP
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(300, 300))
		
		# Open GUI in center of window
		self.Center()
		self.SetBackgroundColour('white')
		
		self.establishMenu()
		
		# Welcome text and line
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		
		titleText = wx.StaticText(self, -1, "Vocabulary Parser",(100,25))
		
		# heading.Center()
		# heading.SetFont(font)
		
		# wx.StaticLine(self, -1, (25, 50), (300,1))
		# 
		
		self.establishButtons()
		

## -------------------------------------------------------------	
class MyApp(wx.App):
	# Actual app runs from here! (Equivalent to main?)
	def OnInit(self):
		frame = MyGUI(None, -1, 'GUI.py')
		frame.Show(True)
		return True

		
def main():
	# GET USER INPUT FOR THESE VARIABLES
	myGlobals.init_globals('LANAAAAAA@gmail.com','WHAT?!', 'imap.googlemail.com', 'C:\----\WordOfDayVocab.txt')
	# print "Executing IMAP connection..."
	# executeIMAP()
	# print "Executing POP3 connection..."
	# executePOP()

	print "\nCyril Figgins\n"
	
	app = MyApp(0)
	app.MainLoop()
	
	print "Window Closed"

if __name__ == "__main__": main()
    