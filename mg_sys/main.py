import time
import email
import mg_receive
import mg_send
import api_42qu
import mg_process
from mg_util import connection, get_userid, get_groupid, get_status
from mg_util import USER_PERMISSION, GROUP_PERMISSION
from mg_util import get_group_address, parse_email_header
from mg_util import encode_header, save_topic, save_mail, process_payload

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global work_c
work_c = connection()

mail_from = 'mail@forpm.net'

def g_mail(rmail, para):
    user_id = para[0]
    group_id = para[1]
    topic_id = para[2]

    smail = process_payload(rmail)
    mail_to = get_group_address(user_id, group_id)
    """
    message_id = rmail['Message-id']
    if message_id:
        smail['In-Reply-To'] = message_id
    """
    smail['To'] = mail_to
    smail['Subject'] = rmail['Subject']
    smail['X-User'] = str(user_id)
    smail['X-Group'] = str(group_id)
    smail['X-Topic'] = str(topic_id)
    return smail

def auto(DEBUG=False):
    if not DEBUG:
        while True:
            data = mg_receive.get_new_mail()
            if data != False:
                for rmail in data:
                    subject = parse_email_header(rmail['Subject'])
                    if subject.lower() == 'system':
                        smail = mg_process.system_mail(rmail)
                    else:
                        para = save_mail(rmail)
                        smail = g_mail(rmail, para)
                    to_addrs = smail['To'].split(',')
                    print to_addrs
                    mg_send.sendmail(mail_from, to_addrs, smail)
            time.sleep(5)
            print time.time()
    else:
        file = open('test/mg_process.eml', 'r')
        rmail = email.message_from_file(file)
        subject = parse_email_header(rmail['Subject'])
        if subject.lower() == 'system':
            smail = mg_process.system_mail(rmail)
        else:
            para = save_mail(rmail)
            smail = g_mail(rmail, para)
        to_addrs = smail['To'].split(',')
        print to_addrs
        mg_send.sendmail(mail_from, to_addrs, smail)

if __name__ == '__main__':
    auto()

