##
##import smtplib
##import time
##import imaplib
##import email
##
### -------------------------------------------------
###
### Utility to read email from Gmail Using Python
###
### ------------------------------------------------
##
##def read_email_from_gmail():
##    try:
##        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
##        mail.login(FROM_EMAIL,FROM_PWD)
##        mail.select('inbox')
##
##        type, data = mail.search(None, 'ALL')
##        mail_ids = data[0]
##
##        id_list = mail_ids.split()   
##        first_email_id = int(id_list[0])
##        latest_email_id = int(id_list[-1])
##
##
##        for i in range(latest_email_id,first_email_id, -1):
##            typ, data = mail.fetch(i, '(RFC822)' )
##
##            for response_part in data:
##                if isinstance(response_part, tuple):
##                    msg = email.message_from_string(response_part[1])
##                    email_subject = msg['subject']
##                    email_from = msg['from']
##                    print ('From : ' + email_from + '\n')
##                    print ('Subject : ' + email_subject + '\n')
##
##    except Exception, e:
##        print str(e)
##


import poplib
from string import random
import StringIO, rfc822
import logging

SERVER = "pop.gmail.com"
USER  = "guydvir.tech@gmail.com"
PASSWORD = "kupelu9e"

# connect to server
logging.debug('connecting to ' + SERVER)
server = poplib.POP3_SSL(SERVER)
#server = poplib.POP3(SERVER)

# login
logging.debug('logging in')
server.user(USER)
server.pass_(PASSWORD)

# list items on server
logging.debug('listing emails')
resp, items, octets = server.list()

# download the first message in the list
id, size = string.split(items[0])
resp, text, octets = server.retr(id)

# convert list to Message object
text = string.join(text, "\n")
file = StringIO.StringIO(text)
message = rfc822.Message(file)

# output message
print(message['From']),
print(message['Subject']),
print(message['Date']),
#print(message.fp.read())   
