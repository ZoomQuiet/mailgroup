import time
import os.path
import os
import re
import MySQLdb
import email
import email.header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import api_42qu
import mg_log
import ConfigParser

op_log = mg_log.tempLogger()

def connection():
    config = ConfigParser.RawConfigParser()
    path = os.path.normpath(os.path.join(os.getcwd(), __file__))
    config.read(os.path.split(path)[0] + '/local_email.cfg')
    host = config.get('database','host')
    user = config.get('database','user')
    passwd = config.get('database','passwd')
    db = config.get('database','db')
    work_db = MySQLdb.connect(host="127.0.0.1", user="root",\
                              passwd="root", db="mailgroup" ,charset="utf8")
    work_c = work_db.cursor()
    return work_c

GROUP_PERMISSION = 99
USER_PERMISSION = 1

global work_c
work_c = connection()


def parse_email_payload(mail_message):
    """Return the email payload that human can read

    Example:

    Args:
        mail_message: the email.message object

    Return:
        the dict of payload that is easy to read
    """
    payload_dict = {}
    if mail_message.is_multipart():
        for content in mail_message.get_payload():
            charset = content.get_charsets()[0]
            payload = content.get_payload(decode=True).decode(charset)
            payload_dict['%s'%content.get_content_subtype()] = payload
    else:
        payload_dict['%s'%mail_message.get_content_subtype()] = \
        mail_message.get_payload(decode=True).decode(mail_message.get_charsets()[0])

    return payload_dict

def parse_email_header(header):
    """parse the email header 

    Args:
        header: the mail_message['Subject']

    Return:
        the human reade subject
    """
    title, code = email.header.decode_header(header)[0]
    # if the title is pure asc-ii, the code is None
    if code == None:
        subject = title
    else:
        subject = title.decode(code)
    return subject


def attach_payload(payload_dict, smail):
    """Encode and attach the payload

    Example

    Args:
        payload_dict: the dict of payload
        smail: the email object for construct

    Return: 
        the email.message object
    """
    for key, data in payload_dict.items():
        smail.attach(MIMEText(data, key, 'utf8'))

    return mail_message

def encode_header(subject):
    """Encode the subject to header
    Args:
        subject:the subject string

    Return:
        the email header
    """
    title = subject.encode('utf-8')
    header = email.header.Header(title, 'utf-8')
    return header

def admin_permission(mailbox):
    config = ConfigParser.RawConfigParser()
    path = os.path.normpath(os.path.join(os.getcwd(), __file__))
    config.read(os.path.split(path)[0] + '/local_email.cfg')
    test_admin = config.get('mailgroup_admin','admin')
    admins = ['silegon@gmail.com',
              'zoom.quiet@gmail.com',
              'zsp007@gmail.com',
              test_admin,]
    if mailbox in admins:
        return True
    else:
        return False

def get_userid(mailbox, add_mailbox=False):
    sql = "select id from mg_user where mailbox='%s';"%mailbox
    if work_c.execute(sql):
        user_id = work_c.fetchone()[0]
        return user_id
    elif add_mailbox:
        url = api_42qu.get_url(mailbox)
        if url:
            sql = "insert into mg_user (signature, mailbox) values('%s', '%s');"
            work_c.execute(sql%(url, mailbox))
            return get_userid(mailbox)
        else:
            op_log.warning("%s isn't 42qu user!"%mailbox)
        return False
    else:
        return False

def get_groupid(gname):
    sql = "select id from mg_group where gname='%s';"%gname
    if  work_c.execute(sql):
        group_id = work_c.fetchone()[0]
        return group_id
    else:
        return False

def get_status(gname, mailbox):
    user_id = get_userid(mailbox)
    group_id = get_groupid(gname)
    sql = "select status from user_group where group_id=%d and user_id=%d"
    if user_id and group_id and work_c.execute(sql%(group_id, user_id)):
        status = work_c.fetchone()[0]
        return status
    else:
        return False

def get_group_address(user_id, group_id):
    sql = "select mg_user.mailbox from mg_user, user_group where\
        user_group.group_id=%s and user_group.user_id=mg_user.id and\
        mg_user.id!=%s;"%(group_id, user_id)
    work_c.execute(sql)
    result = work_c.fetchall()
    address_list = []
    for address in result:
        address_list.append(address[0])
    mail_to = ','.join(address_list)
    return mail_to

def get_signature(mail_from):
    sender = re.search(r'[\w][\w\.]+@[\w\-]+\.[a-zA-Z]{1,4}',
                         mail_from).group()
    sql = "select signature from mg_user where mailbox='%s';"%sender
    work_c.execute(sql)
    signature = work_c.fetchone()[0]
    return signature

def process_payload(rmail):
    payload_dict = parse_email_payload(rmail)
    signature = get_signature(rmail['From'])
    if len(payload_dict)>1:
        smail = MIMEMultipart('alternative')
        for key, value in payload_dict.items():
            # for test ,didn't diferentiate the plain or html
            value += signature
            # encode and attche to mail
            smail.attach(MIMEText(value, key, 'utf-8'))
    else:
        smail = MIMEText(payload_dict.values()[0] + signature,\
                         payload_dict.keys()[0], 'utf-8')
    return smail

def save_topic(rmail, group_id):
    sql = "insert into topic (topic, topic_desc, mailgroup_id) values\
            ('%s', '%s', %s);"
    topic = parse_email_header(rmail['Subject']).encode('utf-8')
    payload_dict = parse_email_payload(rmail)
    topic_desc = payload_dict['plain'][:255].encode('utf-8')
    work_c.execute(sql%(topic, topic_desc, group_id))

    sql = "select max(id) from topic;"
    work_c.execute(sql)
    topic_id = work_c.fetchone()[0]
    return topic_id

def save_mail(rmail):
    user_id = rmail['X-User']
    if not user_id:
        sender = re.search(r'[\w][\w\.]+@[\w\-]+\.[a-zA-Z]{1,4}',
                         rmail['from']).group()
        user_id = get_userid(sender)
        if not user_id:
            return False
    group_id = rmail['X-Group']
    topic_id = rmail['X-Topic']
    if not group_id and not topic_id:
        group_id = 1
             # Because the group id is get by different email
            # but now only one.
        topic_id = save_topic(rmail, group_id)
        
    payload_dict = parse_email_payload(rmail)
    save_mail_dict = {
        'topic_id' : topic_id,
        'message_id' : rmail['Message-id'],
        'create_time' : time.strftime('%Y-%m-%d %H:%M:%S'),
        'body' : payload_dict['plain'].encode('utf-8'),
        'sender_mailbox' : sender,
        'status' : 0, # the status isn't be used now
        'mailgroup' : group_id,
    }
    sql = "insert into mail (topic_id, message_id, body,\
            create_time,\
        sender_mailbox, mailgroup, status) values (%(topic_id)s,\
      '%(message_id)s', '%(body)s', '%(create_time)s',\
       '%(sender_mailbox)s', %(mailgroup)s, %(status)s);"%\
        (save_mail_dict)
    work_c.execute(sql)
    return [user_id, group_id, topic_id]

        
        



