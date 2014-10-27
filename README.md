TransparentLanguage_EmailParser
===============================

Ongoing; Will add GUI soon
--

I have completed two scripts to parse my Gmail inbox for daily Germany vocabulary words/phrases from Transparent Language 
(http://www.transparent.com/). All vocab emails came in the same format as seen in image 'example_email.png'.

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
Update:
I think it'd be nice to have some sort of GUI so users could nicely entire their connection information (username and 
password), and select how they'd like to connect, IMAP or POP3. Ideally, this will also lead to a desktop icon for direct
execution of the script, rather than having to execute from the command line. This will be my chance to learn more about 
creating GUIs (only experienced with Java's swing frames).

I've chosen wxpython over the built-in Tkinter after a cursory Google/Stackoverflow search, wxpython seems to be more 
flexible, provides "out-of-the box" features/widjets, has proven history with the audio recording program 'Audacity' 
(http://www.wxwidgets.org/about/screenshots/ , http://audacity.sourceforge.net/), helpful user community, and native look.

Will start soon!
