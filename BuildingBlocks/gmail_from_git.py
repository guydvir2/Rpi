import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSender:
    def __init__(self, sender='', recipients=[''], body='', attach=[''],
                 password=''):
        self.recipients, self.sender, self.password = recipients, sender, password
        self.body, self.attachments = body, attach
        self.validate()

    def validate(self):
        if self.sender == '':
            with open('user.txt', 'r') as f:
                self.sender = f.read()
                print("Sender details read from file: %s" % self.sender)
        if self.password == '':
            with open('p.txt', 'r') as g:
                self.password = g.read()
        if self.recipients == ['']:
            ask = input('No recipients defined. send to Sender or Abort [S/A]')
            if ask.upper() == 'S':
                self.recipients = [self.sender]
            elif ask.upper() == 'A':
                quit()

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
        # self.attachments = [

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
            print(">>>Email sent!<<<")
            return 1
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            return 0
            raise


if __name__ == '__main__':
    GmailDaemon = GmailSender()#recipients=[''])
    GmailDaemon.compose_mail()
