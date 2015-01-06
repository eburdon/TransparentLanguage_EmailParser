TransparentLanguage_EmailParser
===============================
Ongoing; Project that will be **slowly** solved as the semester
progresses whenever I'm not TOO swamped with homework;

I have completed two scripts to parse my Gmail inbox for daily Germany vocabulary words/phrases from Transparent Language 
(http://www.transparent.com/). All vocab emails come in the same format (as seen in image 'example_email.png').

Both scripts parse the key parts of each email and write them to a file:
  The German word
  The English translation
  Part of speech (Verb, Adjective, etc. ...)
  Example sentence (German)
  Sentence translation (English)

The first script connects, reads, and deletes via a POP3 connection. Unfortunatley, this can only get up to the most
recent 30 messages.

The second script is IMAP-based, and able to handle any number of messages, of any ages. NOTE: This scans the users' ENTIRE 
inbox for the appropriate messages. Currently 'Unread' messages may be incorrectly marked as 'Read' after execution.

At the end of the program execution, users will be asked if they would like to delete the original emails/messages
from their Gmail inbox.

** SPECIAL NOTE
If user has their Gmail IMAP settings set as seen in 'imap_settings_2.png', upon agreeing to delete the original
messages, the emails will be ARCHIVED and not moved to 'TRASH'. They can be found under the 'ALL MAIL' label, and
can be manually moved to 'TRASH' and completely deleted from there.

Alternatively, if user has their Gmail IMAP settings set as seein in 'imap_settings_3.png', upon deleting, the emails
WILL be moved to 'TRASH,' and can be easily deleted from there.

-----------------------------
Update	January 2015:

I wanted to include a nice GUI for users, bonus for providing me
some practical experience creating a basic interface. Ideally, this
will lead to creating a desktop icon/program that one could execute
to clean up an email inbox.

I've chosen to implement this gui using wxpython instead of built-in
(python) Tkinter after a cursory Google/Stackoverflow search. wxpython seems to be more  flexible, provides "out-of-the box" features/widjets, has proven history with the audio recording program 'Audacity' (http://www.wxwidgets.org/about/screenshots/ , http://audacity.sourceforge.net/), helpful user community, and native look.

Image has been included showing current state of the GUI & sample
of what is still appearing at the command-line interface.

The main window (larger) has a welcome message, and two buttons a
user can click to parse their email. 

The 'quit' option under Menu > File, is operational; will likely
remove 'save' and 'open' since they don't apply.

Edit menu has some checkmark options, but I want to make the 'Options' item (currently opens a new, plain window) to be where user set their preferences (e.g., username & password?)


FUTURE TASKS
------------
	> Get user input for email/password (currently hard coded into GUI.PY)
	
	> Display dynamic script messages (e.g., words found, "Would you like to delete these emails...") within the main GUI frame
	
	> Add minor documentation/FAQ under 'help'
	
	> Complete 'set preferences' window (menu > edit > options)
