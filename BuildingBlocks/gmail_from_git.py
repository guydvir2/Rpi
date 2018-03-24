import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSender:
    def __init__(self, sender='', password='', pfile='', ufile=''):
        self.pfile, self.ufile = pfile, ufile

        if sender == '':
            if os.path.isfile(self.ufile) is True:
                with open(self.ufile, 'r') as f:
                    self.sender = f.read()
                    print(">> Sender details read from file: %s" % self.sender)
            else:
                self.sender = input("Please enter a gmail sender: ")
                # print('>> file containing user email details- not found.\n>> quitting...')
                # quit()
        else:
            self.sender = sender
        if password == '':
            if os.path.isfile(self.pfile) is True:
                with open(self.pfile, 'r') as g:
                    self.password = g.read()
                    print(">> Password read from file")
            else:
                self.password = input("Password: ")
                # print('>> file containing password details- not found.\n>> quitting...')
                # quit()
        else:
            self.password = password

    def compose_mail(self, subject='', body='', attach=[''], recipients=['dr.guydvir@gmail.com']):
        # Create the enclosing (outer) message
        self.body, self.attachments = body, attach
        self.recipients = recipients
        if subject == '':
            ask = input('Enter subject: ')
            if ask == '':
                subject = "Automated email"
            else:
                subject = ask

        COMMASPACE = ', '
        self.outer = MIMEMultipart()
        self.outer['Subject'] = subject
        self.outer['To'] = COMMASPACE.join(self.recipients)
        self.outer['From'] = self.sender
        body = MIMEText(self.body)  # convert the body to a MIME compatible string
        self.outer.attach(body)  # attach it to your main message
        self.outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        self.file_attachments()
        self.send()

    def file_attachments(self):
        # List of attachments
        # self.attachments = ['/Users/guy/log.log']

        # Add the attachments to the message
        if self.attachments != ['']:
            for file in self.attachments:
                if os.path.isfile(file) is True:
                    try:
                        with open(file, 'rb') as fp:
                            msg = MIMEBase('application', "octet-stream")
                            msg.set_payload(fp.read())
                        encoders.encode_base64(msg)
                        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                        self.outer.attach(msg)
                    except FileNotFoundError:
                        print(">> Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                        raise
                else:
                    ask = input(">> Attachment not found, send anyway [y/n]?")
                    if ask.upper() == 'N':
                        print("quit!")
                        quit()

    def send(self):
        # Send the email
        self.composed = self.outer.as_string()
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(self.sender, self.password)
                s.sendmail(self.sender, self.recipients, self.composed)
                s.close()
            print(">> Email sent!")
        except:
            print(">> Unable to send the email. Error: ", sys.exc_info()[0])
            raise


if __name__ == '__main__':
    GmailDaemon = GmailSender(pfile='p.txt', ufile='user.txt')
    GmailDaemon.compose_mail(recipients=['guy.ipaq@gmail.com'], attach=[''], body="This is an automated email")
