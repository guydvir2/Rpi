import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSender:
    def __init__(self, sender='', recipients=['dr.guydvir@gmail.com'], body='', attach=[''],
                 password=''):
        self.recipients = recipients
        self.body, self.attachments = body, attach
        if sender == '':
            with open('user.txt', 'r') as f:
                self.sender = f.read()
                print("Sender details read from file: %s" % self.sender)
        else:
            self.sender = sender
        if password == '':
            with open('p.txt', 'r') as g:
                self.password = g.read()
        else:
            self.password = password
            print(type(self.password))

    def compose_mail(self):
        # Create the enclosing (outer) message
        COMMASPACE = ', '
        self.outer = MIMEMultipart()
        self.outer['Subject'] = 'Hi from guy'
        self.outer['To'] = COMMASPACE.join(self.recipients)
        self.outer['From'] = self.sender
        body = 'This is the body of the email.'
        self.body = MIMEText(body)  # convert the body to a MIME compatible string
        self.outer.attach(self.body)  # attach it to your main message
        self.outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        self.file_attachments()
        self.send()

    def file_attachments(self):
        # List of attachments
        self.attachments = ['/Users/guy/log.log']

        # Add the attachments to the message
        if self.attachments != ['']:
            for file in self.attachments:
                try:
                    with open(file, 'rb') as fp:
                        msg = MIMEBase('application', "octet-stream")
                        msg.set_payload(fp.read())
                    encoders.encode_base64(msg)
                    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                    self.outer.attach(msg)
                except:
                    print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                    raise

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
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise


if __name__ == '__main__':
    GmailDaemon = GmailSender(recipients=['guy.ipaq@gmail.com'])
    GmailDaemon.compose_mail()
