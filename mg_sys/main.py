import time
import email
import mg_receive
import mg_send
import parse_mail
import generate_mail
import api_42qu
import mg_process

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_from = 'silegon@gmail.com'
mail_to = 'silegon@gmail.com'

def g_mail(rmail):

    extra_info = api_42qu.get_url(rmail['From'])
    subject = parse_mail.parse_email_header(rmail['Subject'])
    if subject.lower() == 'system':
        return mg_process.system_mail(rmail)
    else:
        payload_dict = parse_mail.parse_email_payload(rmail)
        
        if len(payload_dict)>1:
            smail = MIMEMultipart('alternative')
            for key, value in payload_dict.items():
                # for test ,didn't diferentiate the plain or html
                value += extra_info
                # encode and attche to mail
                smail.attach(MIMEText(value, key, 'utf-8'))
        else:
            smail = MIMEText(payload_dict.values()[0] + extra_info,\
                             payload_dict.keys()[0], 'utf-8')

        smail['Subject'] = generate_mail.encode_header(subject)
        return smail

def auto():
    #while True:
    for i in range(1):
        data = mg_receive.get_new_mail()
        print data
        if data != False:
            for rmail in data:
                smail = g_mail(rmail)
                print smail.as_string()
                mg_send.sendmail(mail_from, smail['To'], smail)

if __name__ == '__main__':
    auto()

