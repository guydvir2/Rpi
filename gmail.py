##import smtplib
##
##gmail_user = 'guydvir.tech@gmail.com'  
##gmail_password = 'kupelu9e'
##
##try:  
##    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
##    server.ehlo()
##    server.login(gmail_user, gmail_password)
##except:  
##    print ('Something went wrong...')


import smtplib

gmail_user = 'guydvir.tech@gmail.com'  
gmail_password = 'kupelu9e'

sent_from = gmail_user  
to = ['guydvir2.gmail.com', 'guy.ipaq@gmail.com']  
subject = 'OMG Super Important Message'  
body = 'hey you donkey'

email_text = """\  
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email sent!')
except:  
    print ('Something went wrong...')
