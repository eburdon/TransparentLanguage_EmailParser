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
#		website:	web.uvic.ca/~eburdon
#		LinkedIn:	/in/eburdon
#		Riipen:		/users/1017
########

import wx

# Import MY modules
import myGlobals
from   exec_imap import executeIMAP
from   exec_POP  import executePOP


class MyGUI(wx.Frame):

	# GET INFO FROM myGlobals.py --------------------------------
	
	def getCurrentUsername(self, usernameStatus):
		if (len(myGlobals.usrnm) != 0 ):
			# If a username has been found, change default text display value.
			usernameStatus=myGlobals.usrnm
		self.userNameBox.SetValue(usernameStatus)
	
	def getCurrentPassword(self, passwordStatus):
		if (len(myGlobals.usrpss) != 0):
			passwordStatus = myGlobals.usrpss
		self.passwordBox.SetValue(passwordStatus)
	
	def getDefaultFilename(self):
		filenameStatus = myGlobals.saveToFile
		self.filenameBox.SetValue(filenameStatus)
	
	def getDefaultConnection(self):
		connectionStatus = myGlobals.host
		self.connectionBox.SetValue(connectionStatus)	
		
		
	# MENU/BUTTON OPERATIONS ------------------------------------
	
	def OnQuit(self, event):
		self.Close()
		
	def OnCancel(self, event):
		self.Destroy()
	
	def ProceedToSettings(self, event):
		# Get rid of text boxes
		self.userNameBox.Destroy()
		self.passwordBox.Destroy()
		# Get rid of Buttons
		self.GetUsernameButton.Destroy()
		self.GetPasswordButton.Destroy()
		self.quitButton.Destroy()
		self.proceedButton.Destroy()
		
		self.settingsButtons()
		
	def ProceedToParser(self,event):
		self.connectionBox.Destroy()
		self.filenameBox.Destroy()
		
		self.getFileNameButton.Destroy()
		self.getConnectionButton.Destroy()
		self.quitButton.Destroy()
		self.proceedButton.Destroy()
		
		self.initParsingOptions()
	
	def runIMAP(self, event):
		self.hideParsingButtons()
		executeIMAP(self)
		self.showFinishMessage()
		
	def runPOP(self, event):
		self.hideParsingButtons()
		executePOP()
		self.showFinishMessage()
		
	def getPassword(self, event):
		passDial = wx.TextEntryDialog(self.panel, 'What is your password?', "PASSWORD ENTRY", "", style=wx.OK)
		passDial.ShowModal()
		PASSWORDENTRY = passDial.GetValue()
		passDial.Destroy()
		
		# Assign; For security reasons, do not display the password
		myGlobals.usrpss = PASSWORDENTRY
		if (len(PASSWORDENTRY)!= 0):
			self.updateCurrentPassword(self.passwordBox, "Password Found")
			
	def getUsername(self, event):
		usrDial = wx.TextEntryDialog(self.panel, 'What is your username?', "USERNAME ENTRY", "", style=wx.OK)
		usrDial.ShowModal()
		LOGINNAME = usrDial.GetValue()
		usrDial.Destroy()
		
		# Assign and update display!
		myGlobals.usrnm = LOGINNAME
		if (len(LOGINNAME)!=0):
			self.updateCurrentUsername(self.userNameBox, myGlobals.usrnm)
	
	def getNewSaveFile(self, event):
		fileDial = wx.TextEntryDialog(self.panel, 'What file are you saving to?', "FILE NAME ENTRY", "", style=wx.OK)
		fileDial.ShowModal()
		SAVEFILEENTRY = fileDial.GetValue()
		fileDial.Destroy()

		# Ensure user typed something in
		if (len(SAVEFILEENTRY)!= 0):
			myGlobals.set_saveFile(SAVEFILEENTRY)
			self.updateSaveFileDisplay()
		else:
			wx.MessageBox('You must include a file to save to!', 'Alert!', wx.OK)
			getNewSaveFile(self, event)

	def getNewConnection(self, event):
		connDial = wx.TextEntryDialog(self.panel, 'What server will you connect to?', "CONNECTION ENTRY", "", style=wx.OK)
		connDial.ShowModal()
		SAVECONNENTRY = connDial.GetValue()
		connDial.Destroy()
		
		if (len(SAVECONNENTRY)!=0):
			myGlobals.set_host(SAVECONNENTRY)
			self.updateConnectionDisplay()
		else:
			wx.MessageBox('You must include a connection host!', 'Alert!', wx.OK)
			getNewConnection(self,event)
		
	def updateSaveFileDisplay(self):
		self.filenameBox.SetValue(myGlobals.saveToFile)
	
	def updateConnectionDisplay(self):
		self.connectionBox.SetValue(myGlobals.host)
	
	def updateCurrentUsername(self, userNameBox, newName):
		self.userNameBox.SetValue(newName)

	def updateCurrentPassword(self, passwordBox, passwordStatus):
		# For Security reasons, DO NOT DISPLAY THE PASSWORD ("Password Found")
		self.passwordBox.SetValue(passwordStatus)


	# WIDGET DISPLAY ACTIONS -------------------
	def hideParsingButtons(self):
		self.popButton.Hide()
		self.imapButton.Hide()
		self.welTwo.Hide()
		progStatus = "Processing..."
		self.RunMsg = wx.StaticText(self.panel,label=progStatus, pos = (10,30))
		self.RunMsg.Show()

	def showParsingButtons(self):
		self.popButton.Show()
		self.imapButton.Show()
		self.RunMsg.Destroy()
		self.welTwo.Show()
	
	def showFinishMessage(self):
		wx.MessageBox('Successfully finished!', 'Info', wx.OK | wx.ICON_INFORMATION)
		# self.showParsingButtons()
		
	def establishParsingButtons(self):
		self.imapButton = wx.Button(self.panel, label='IMAP', pos=(75, 100))
		self.imapButton.Bind(wx.EVT_BUTTON, self.runIMAP)
		
		self.popButton = wx.Button(self.panel, label='POP3', pos=(175, 100))
		self.popButton.Bind(wx.EVT_BUTTON, self.runPOP)

	def establishQuitProceedButtons(self, sn):
		# sn = screen ID number
		self.proceedButton = wx.Button(self.panel, label='PROCEED', pos=(60, 110))
		self.quitButton = wx.Button(self.panel, label='QUIT', pos=(170, 110))
		self.quitButton.Bind(wx.EVT_BUTTON, self.OnQuit)
		if (sn == 1):
			self.proceedButton.Bind(wx.EVT_BUTTON, self.ProceedToSettings)
		elif (sn == 2):
			self.proceedButton.Bind(wx.EVT_BUTTON, self.ProceedToParser)
		
			
	# FIRST SCREEN -----------------------------
	def initialButtons(self, panel, sizer):
		# CURRENT Username information
		usernameStatus = "NO USERNAME SET" 		# Default
		# Create read-only text box (display information)
		self.userNameBox = wx.TextCtrl(self.panel, -1, size=(135,-1), pos=(25, 80), style = wx.TE_READONLY)
		self.getCurrentUsername(usernameStatus)
		
		# Update username button
		self.GetUsernameButton = wx.Button(panel, label='UPDATE USERNAME', pos=(25, 50))
		self.GetUsernameButton.Bind(wx.EVT_BUTTON, self.getUsername)
		
		#----
		
		# CURRENT Password information
		passwordStatus = "NO PASSWORD FOUND"	# Default
		self.passwordBox = wx.TextCtrl(self.panel, -1, size=(135,-1), pos=(170, 80), style = wx.TE_READONLY)
		self.getCurrentPassword(passwordStatus)
		
		# Update password option
		self.GetPasswordButton = wx.Button(panel, label='CHANGE PASSWORD', pos=(170, 50))
		self.GetPasswordButton.Bind(wx.EVT_BUTTON, self.getPassword)
		
		self.establishQuitProceedButtons(1)
		
	# SECOND SCREEN
	def settingsButtons(self):
		# CURRENT FILE SAVE INFORMATION
		self.filenameBox = wx.TextCtrl(self.panel, -1, size=(135,-1), pos=(25, 80), style = wx.TE_READONLY)
		self.getDefaultFilename()
		# Button
		self.getFileNameButton = wx.Button(self.panel, label='Change save file?', pos=(25, 50))
		self.getFileNameButton.Bind(wx.EVT_BUTTON, self.getNewSaveFile)
		
		# CURRENT CONNECTION INFORMATION
		self.connectionBox = wx.TextCtrl(self.panel, -1, size=(135,-1), pos=(170, 80), style = wx.TE_READONLY)
		self.getDefaultConnection()
		#Button
		self.getConnectionButton = wx.Button(self.panel, label='Change connection?', pos=(170, 50))
		self.getConnectionButton.Bind(wx.EVT_BUTTON, self.getNewConnection)
		
		self.establishQuitProceedButtons(2)
	
	# THIRD SCREEN
	def initParsingOptions(self):
		txtTwo = "Would you like an IMAP or POP3 connection?"
		self.welTwo = wx.StaticText(self.panel,label=txtTwo, pos = (10,30))
		self.establishParsingButtons()
	
	
	## BASE FRAME/WINDOWS -------------------------------------------------
	
	# Opens/Launches separate window
	def editFrame(self, event):
		frame  = editingFrame()
		frame.Show()
		print "Opened edit window"

	# Create & attach a menu bar; implements normal, check, and radio items
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
	
	# Add welcome messages to 'header' of window; BASE SCREEN
	def initalizeMainFrame(self, panel, sizer):
		txtOne = "Welcome to my Transparent Language email parser!"
		self.welOne  = wx.StaticText(panel,label=txtOne, pos = (10,10))
	
	# --- GUI CONSTRUCTOR --
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(350, 250))
		
		# Frame settings 
		self.Center()			# Open GUI in center of window
		self.SetBackgroundColour('white')	# Define background
		
		self.panel = wx.Panel(self)
		self.sizer = wx.GridBagSizer(5,5)
		
		# Contruct Frame
		self.establishMenu()
		self.initalizeMainFrame(self.panel, self.sizer)
		
		self.initialButtons(self.panel, self.sizer)
		
		# Static line not working??
		wx.StaticLine(self, -1, (25,30), (300,1), style=wx.LI_HORIZONTAL)
		
		self.border = wx.BoxSizer()
		self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 25)
		

## -------------------------------------------------------- ##
class MyApp(wx.App):
	# Actual app inits from here! (Equivalent to main?)
	def OnInit(self):
		frame = MyGUI(None, -1, 'Transparent Language Email Parser')
		frame.Show(True)
		return True

## --------------------------------------------------------	##
class editingFrame(wx.Frame):
	""""""
	# OPENS IN NEW WINDOW
	def __init__(self):
		# Constructor
		wx.Frame.__init__(self, None, title="Set preferences")
		panel = wx.Panel(self)
		txt = wx.StaticText(panel, label = "Lying is like, 95% of what I do.")

## -------------------------------------------------------- ##
def main():
	# GET USER INPUT FOR THESE VARIABLES?
	myGlobals.init_globals('','')
	
	# Open application class/constructor
	app = MyApp(0)
	
	# Run application
	app.MainLoop()

if __name__ == "__main__": main()
    