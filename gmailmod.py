import smtplib


def sendmail(recipient, subject, body):
    gmail_user = "guydvir.tech@gmail.com"
    gmail_pwd = "kupelu9e"
    FROM = "GuyDvir@Linux"
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body +"\nSent by PythonGmail"

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        # print('successfully sent the mail')
    except:
        print("failed to send mail")