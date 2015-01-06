#!/usr/bin/python

# GUI.py

#	User Interface for Transparent Language daily message
#	parsing

#### Written by:
#        Erika Burdon
#        Software Engineering Student
#        University of Victoria             BC, CANADA
#        https://github.com/eburdon
#        eburdonGIT@gmail.com
#        All comments and critques on this script are welcome!
#
#		LinkedIn:	/in/eburdon
#		Riipen:		/users/1017
########

import wx
import myGlobals
from exec_imap import executeIMAP
from exec_POP import executePOP


class MyGUI(wx.Frame):

	# MENU/BUTTON OPERATIONS
	def OnQuit(self, event):
		self.Close()
	
	def runIMAP(self, event):
		executeIMAP()
		self.showFinishMessage()
		
	def runPOP(self, event):
		executePOP()
		self.showFinishMessage()
	
	def showFinishMessage(self):
		wx.MessageBox('Successfully finished!', 'Info', wx.OK | wx.ICON_INFORMATION)
	
	# Opens/Launches separate window for potential options
	def editFrame(self, event):
		frame  = editingFrame()
		frame.Show()
		print "Opened edit window"
	

	# Create & attach a menu bar; implements normal, check, and
	#	radio items
	def establishMenu(self):

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


		
	# Position two executable buttons below welcome message
	def establishButtons(self, panel, sizer):
		self.imapButton = wx.Button(panel, label='IMAP', pos=(75, 100))
		self.imapButton.Bind(wx.EVT_BUTTON, self.runIMAP)
		
		self.popButton = wx.Button(panel, label='POP3', pos=(175, 100))
		self.popButton.Bind(wx.EVT_BUTTON, self.runPOP)
		
	
	# Add welcome messages to 'header' of window
	def initalizeMainFrame(self, panel,sizer):
		txtOne = "Welcome to my Transparent Language email parser!"
		txtTwo = "Would you like an IMAP or POP3 connection?"
		
		self.welOne  = wx.StaticText(panel,label=txtOne, pos = (10,10))
		self.welTwo = wx.StaticText(panel,label=txtTwo, pos = (10,30))
	
	
	# --- GUI CONSTRUCTOR --
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(325, 200))
		
		# Frame settings 
		self.Center()			# Open GUI in center of window
		
		self.SetBackgroundColour('white')	# Define background
		
		self.panel = wx.Panel(self)
		
		self.sizer = wx.GridBagSizer(5,5)
		
		# Contruct Frame
		self.establishMenu()
		self.initalizeMainFrame(self.panel, self.sizer)
		
		# Add buttons
		self.establishButtons(self.panel, self.sizer)
		
		self.border = wx.BoxSizer()
		self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 25)
		

## --------------------------------------------------------	
class MyApp(wx.App):
	# Actual app inits from here! (Equivalent to main?)
	def OnInit(self):
		frame = MyGUI(None, -1, 'Transparent Language Email Parser')
		frame.Show(True)
		return True

## --------------------------------------------------------	
class editingFrame(wx.Frame):
	""""""
	# OPENS IN NEW WINDOW
	def __init__(self):
		# Constructor
		wx.Frame.__init__(self, None, title="Set preferences")
		panel = wx.Panel(self)
		txt = wx.StaticText(panel, label = "Lying is like, 95% of what I do.")
	
##############################################################
def main():
	# GET USER INPUT FOR THESE VARIABLES?
	myGlobals.init_globals('LANAAAAAAAAA@gmail.com','WHAT?!', 'imap.googlemail.com', 'dangerzone.txt')
	
	# Open application class/constructor
	app = MyApp(0)
	
	# Run application
	app.MainLoop()

if __name__ == "__main__": main()
    