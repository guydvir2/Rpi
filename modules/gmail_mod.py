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

    def __init__(self, sender=None, password=None, password_file=None, sender_file=None):
        self.pfile, self.ufile = password_file, sender_file
        self.sender, self.password, self.recipients = sender, password, None
        self.subject, self.attachments = None, ''
        self.values, self.keys = [], []
        self.send_result, self.success_load = None,None
        self.temp_body = ''

        self.get_account_credits()

    def get_account_credits(self):
        # case 1: user deails from file
        if self.sender is None and self.ufile is not None:
            if os.path.isfile(self.ufile) is True:
                with open(self.ufile, 'r') as f:
                    self.sender = f.read()
                    # print(">> Sender details read from file: %s" % self.sender)
            else:
                self.sender = input("Please enter a gmail sender: ")
        # case 2: not supplied details
        elif self.sender is None and self.ufile is None:
            self.sender = input("Please enter a gmail sender: ")

        # Case 1 - - detals from file
        if self.password is None and self.pfile is not None:
            if os.path.isfile(self.pfile) is True:
                with open(self.pfile, 'r') as g:
                    self.password = g.read()
                    # print(">> Password read from file")
            else:
                self.password = getpass.getpass("Password: ")
        elif self.password is None and self.pfile is None:
            self.password = getpass.getpass("Password: ")

    def compose_mail(self, subject='', body='', attach=[''], recipients=['']):
        # Create the enclosing (outer) message
        self.body, self.attachments = body, attach
        self.recipients, self.subject = recipients, subject

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
        if body == '':
            self.body = input('Enter Body of email: ')

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

    def add_body(self, msg):
        self.temp_body = self.temp_body+'\n'+msg
        
    def finalize_body(self, msg):
        body = MIMEText(msg)  # convert the body to a MIME compatible string
        self.outer.attach(body)  # attach it to your main message
        self.outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    def file_attachments(self):
        # List of attachments
        if self.attachments != ['']:
            self.add_body('\nAttached files:')
            self.add_body('~~~~~~~~~~~~~~~')
            for i, file in enumerate(self.attachments):
                if os.path.isfile(file) is True:
                    try:
                        prefix = ''
                        with open(file, 'rb') as fp:
                            msg = MIMEBase('application', "octet-stream")
                            msg.set_payload(fp.read())
                        encoders.encode_base64(msg)
                        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                        self.outer.attach(msg)
                    except FileNotFoundError:
                        print(">> Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                        prefix = 'failed: '
                        raise
                else:
                    prefix = 'failed: '
                    ask = input(">> Attachment not found, send anyway [y/n]?")
                    self.attachments[i] = 'fail to send: ' + self.attachments[i]
                    if ask.upper() == 'N':
                        print("quit!")
                        quit()
                self.add_body(('file #%d/%d: %s' % (i + 1, len(self.attachments), 
                                                    prefix + file)))
            self.add_body('~~~~~~~~~~~~~~~')

        else:
            pass
            #self.add_body('No attached files')

    def send(self, summ=False):
        # Send the email
        if summ is True:
            self.sum_of_send()
                        
        self.add_body('\n*** end of e-mail ***')
        self.finalize_body(self.temp_body)
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
            self.send_result = True
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            self.send_result = False
        finally:
            self.body, self.temp_body = '',  ''
            pass
            #self.sum_of_send()

    def time_stamp(self):
        a = str(datetime.datetime.now())[:-5]
        return a

    def sum_of_send(self):
        out_dict = {}
        self.keys = ['time', 'recipients', 'account', 'attachments', 'subject', 'success']
        self.values = [self.time_stamp(), self.recipients, self.sender, self.attachments, self.subject,
                       self.send_result]

        for i, key in enumerate(self.keys):
            out_dict[key] = self.values[i]
            self.add_body('~' + str(key) + ': ' + str(out_dict[key]))
        # return out_dict


class MailBox:
    def __init__(self):
        self.inbox = []
        self.outbox = []
        self.sent = []

    def add_mail(self, subject, msg, destination):
        time = str(datetime.datetime.now())[0:-5]
        self.inbox.append({'subject': subject, 'msg': msg, 'dest': destination, 'time': time})
        # print(self.inbox)
        self.move_sent_item(self.inbox[-1])

    def move_sent_item(self, mail_item):
        time = str(datetime.datetime.now())[0:-5]
        self.sent.append(mail_item)
        print("mail sent", self.sent[-1])


if __name__ == '__main__':
    path = '/home/guy/Documents/github/Rpi/modules/'
    GmailDaemon = GmailSender(sender_file=path + 'ufile.txt',
                              password_file=path + 'pfile.txt')
    #GmailDaemon = GmailSender (sender='guydvir.tech@gmail.com', password='G345345')
    GmailDaemon.compose_mail(recipients=['dr.guydvir@gmail.com'], body="Python automated email",
                             subject='Hi from gmail application in Python', attach=[''])
    # a = MailBox()
    # a.add_mail('this is subject', 'this is my msg', 'and this is my destiantion')
    # a.add_mail('this is subject2', 'this is my msg2', 'and this is my destiantion2')
