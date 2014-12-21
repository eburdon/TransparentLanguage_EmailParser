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
	
	def editFrame(self, event):
		# Launch a new edit window
		frame  = editingFrame()
		frame.Show()
		print "Opened edit window"
	
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
		
		editOptions = wx.MenuItem(edit, 203, '&Options', 'Set your preferences')
		edit.AppendItem(editOptions)
		self.Bind(wx.EVT_MENU, self.editFrame, id=203)
		
		## HELP MENU ------------------------------------------
		help.Append(301, 'Help item 1', 'Dosomething useful')
		
		# ADD SUBMENUS to MENU --------------------------------
		topmenubar.Append(file, '&File')
		topmenubar.Append(edit, '&Edit')
		topmenubar.Append(help, '&Help')
		
		# CONSTRUCT menubar in application --------------------
		self.SetMenuBar(topmenubar)
		
	def establishButtons(self, panel):
		pnl = wx.Panel(self)
		
		imapButton = wx.Button(pnl, label='IMAP', pos=(20,30))
		imapButton.Bind(wx.EVT_BUTTON, self.runIMAP)
		
		popButton = wx.Button(pnl, label='POP3', pos=(50,60))
		popButton.Bind(wx.EVT_BUTTON, self.runPOP)
	
	def initalizeMainFrame(self, panel):
		self.welcome = wx.StaticText(self.panel,label=self.welcomeText)
	
	
	# --- GUI CONSTRUCTOR --
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(300, 300))
		
		self.welcomeText = "Welcome to my TransparentLanguage email parser. \n\t\tIMAP or POP3?"
		
		self.Center()			# Open GUI in center of window
		self.SetBackgroundColour('white')	# Define background
		self.panel = wx.Panel(self)			# Attaching Panel
		
		# Set sizer of frame, so we can change frame size to match
		#	widgets
		self.windowSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
		self.sizer = wx.GridBagSizer(5,5)
		
		# BEGIN FRAME CONSTRUCTION
		self.establishMenu()
		self.initalizeMainFrame(self.panel)
		self.establishButtons(self.panel)
		
		self.button = wx.Button(self.panel, label = "TEST")
		self.buttonT = wx.Button(self.panel, label = "TEST2")
		
		#self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
		# self.sizer = wx.GridBagSizer(5,5)
		self.sizer.Add(self.welcome, (0,0))
		
		# self.sizer.Add(self.button, (1,0),(1,2))
		self.sizer.Add(self.button, (1,0),(1,2))
		self.sizer.Add(self.buttonT, (2,1),(1,2))
		
		self.border = wx.BoxSizer()
		self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 25)
		
		# Use the sizers
		self.panel.SetSizerAndFit(self.border)
		self.SetSizerAndFit(self.windowSizer)
		
		

## --------------------------------------------------------	
class MyApp(wx.App):
	# Actual app runs from here! (Equivalent to main?)
	def OnInit(self):
		frame = MyGUI(None, -1, 'GUI.py')
		frame.Show(True)
		return True

## --------------------------------------------------------	
class editingFrame(wx.Frame):
	""""""
	
	def __init__(self):
		# Constructor
		wx.Frame.__init__(self, None, title="Set preferences")
		panel = wx.Panel(self)
		txt = wx.StaticText(panel, label = "I'm the one you're looking for")
	
##############################################################
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
    