TransparentLanguage_EmailParser
===============================

<b>Status: </b>Complete - More/Future work can be done but for now, happy with the product.

---------------------------------

I have completed two scripts to parse my Gmail inbox for daily Germany vocabulary words/phrases from Transparent Language 
(http://www.transparent.com/). All vocab emails come in the same format (Visit Wiki's screenshot page for sample email).

Both scripts parse the following key parts of each email and write them to a file:
  * The German word
  * The English translation
  * Part of speech (Verb, Adjective, etc. ...)
  * Example sentence (German)
  * Sentence translation (English)

The first script connects, reads, and deletes via a POP3 connection. Unfortunatley, this can only get up to the most
recent 30 messages.

The second script is IMAP-based, and able to handle any number of messages, of any ages. NOTE: This scans the users' ENTIRE 
inbox for the appropriate messages. Currently 'Unread' messages may be incorrectly marked as 'Read' after execution.

At the end of the program execution, users will be asked if they would like to delete the original emails/messages
from their Gmail inbox. (Command line interface, NOT from GUI.)

<b>Visit WIKI for _run instructions_ and list of _future work_</b>
