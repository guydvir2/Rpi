import os
import sys
import smtplib
import getpass
import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSender:
    """ This class designed to send emails using a gmail accout, including attachments.
    parameters:
    sender/password - as a class parameter or as a text file ufile, pfile
    body - as a class parameter : a text from body of mail
    subject - as a class parameter
    attach - file attachments, as a ['file1','file2']
    recipients - ['recip1','recip2']"""

    def __init__(self, sender=None, password=None, pfile=None,ufile=None):
        self.pfile, self.ufile = pfile, ufile
        self.sender, self.password = sender, password
        self.get_account_credits()

    def get_account_credits(self):
        # case 1: user deails from file
        if self.sender is None and self.ufile is not None:
            if os.path.isfile(self.ufile) is True:
                with open(self.ufile, 'r') as f:
                    self.sender = f.read()
                    print(">> Sender details read from file: %s" % self.sender)
            else:
                print("BVBV")
                self.sender = input("Please enter a gmail sender: ")
        # case 2: not supplied details
        elif self.sender is None and self.ufile is None:
            self.sender = input("Please enter a gmail sender: ")

        # Case 1 - - detals from file
        if self.password is None and self.pfile is not None:
            if os.path.isfile(self.pfile) is True:
                with open(self.pfile, 'r') as g:
                    self.password = g.read()
                    print(">> Password read from file")
            else:
                self.password = getpass.getpass("Password: ")
        elif self.password is None and self.pfile is None:
            self.password = getpass.getpass("Password: ")


    def compose_mail(self, subject='', body='', attach=[''], recipients=['']):
        # Create the enclosing (outer) message
        self.body, self.attachments = body, attach
        self.recipients = recipients

        if self.recipients == ['']:
            ask = input('No recipients defined. send to Sender or Abort [S/A]')
            if ask.upper() == 'S':
                self.recipients = [self.sender]
            elif ask.upper() == 'A':
                quit()

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
            print(">>> Email sent! <<<")
            return 1
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            return 0


if __name__ == '__main__':
    GmailDaemon = GmailSender()  # or directly (sender='send@gmail.com',password='pswd')
    GmailDaemon.compose_mail(recipients=['dr.guydvir@gmail.com'], attach=[''], body="Python automated email",
                             subject='Alarm!')
