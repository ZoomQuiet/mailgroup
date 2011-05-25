import os
import os.path
import smtplib
import ConfigParser

def smtp_connection():
    config = ConfigParser.RawConfigParser()

    path = os.path.normpath(os.path.join(os.getcwd(), __file__))
    config.read(os.path.split(path)[0] + '/local_email.cfg')

    smtp_server = config.get('send_mail','smtp_server')
    smtp_server_port = config.getint('send_mail','smtp_server_port')
    username = config.get('send_mail','username')
    password = config.get('send_mail','password')

    smtpserver = smtplib.SMTP(smtp_server, smtp_server_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(username, password)

    return smtpserver

def sendmail(mailfrom, mailto, mail):
    smtp = smtp_connection()
    smtp.sendmail(mailfrom, mailto, mail.as_string())



