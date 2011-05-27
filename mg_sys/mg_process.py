import re
import email
from email.mime.text import MIMEText
import MySQLdb
import parse_mail
import generate_mail
import api_42qu
import mg_log

log = mg_log.tempLogger()

global work_c
work_db = MySQLdb.connect(host="127.0.0.1", user="root",\
                          passwd="root", db="mailgroup" ,charset="utf8")
work_c = work_db.cursor()

GROUP_PERMISSION = 99
USER_PERMISSION = 1

def get_userid(mailbox):
    sql = "select id from mg_user where mailbox='%s';"%mailbox
    if work_c.execute(sql):
        user_id = work_c.fetchone()[0]
        return user_id
    else:
        url = api_42qu.get_url(mailbox)
        if url:
            sql = "insert into mg_user (signature, mailbox) values('%s', '%s');"
            work_c.execute(sql%(url, mailbox))
            return get_userid(mailbox)
        else:
            log.warning("%s isn't 42qu user!"%mailbox)
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
    
#the status user:1, group_admin:99
def admin_permissions(mailbox):
    admins = ['silegon@gmail.com',
              'zoom.quiet@gmail.com',
              'zsp007@gmail.com',]
    if mailbox in admins:
        return True
    else:
        return False


def admin_op(st, mailbox):
    command = st.pop(0)
    gname = st.pop(0)
    if st:
        mailbox_list = st[0].split(',')
    if command == 'create':
        if get_groupid(gname):
            log.error('mail group %s already exist'%gname)
        else:
            sql = "insert into mg_group (gname) values('%s');"%(gname)
            work_c.execute(sql)
            log.info('mail group %s create succee!'%gname)
    elif command == 'bind':
        for mailbox in mailbox_list:
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            status = get_status(gname, mailbox)
            if status == GROUP_PERMISSION:
                log.error('group %s already exist administator %s'%
                                    (gname, mailbox))
            elif status == USER_PERMISSION:
                sql = 'update user_group set status=%d where group_id=%d\
                      and user_id=%d'%(GROUP_PERMISSION, group_id, user_id)
                work_c.execute(sql)
                log.info('Elevation %s administrator privileges to %s'\
                                    %(mailbox, gname))
            else:
                sql = 'insert into user_group (group_id, user_id, status)\
                        values (%d, %d, %d)'%(group_id, user_id,\
                                              GROUP_PERMISSION)
                work_c.execute(sql)
                log.info('Add administrator %s privileges to %s'\
                                    %(mailbox, gname))
    elif command == 'del':
        for mailbox in mailbox_list:
            status = get_status(gname, mailbox)
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            if status == GROUP_PERMISSION:
                sql = 'update user_group set status=%d where group_id=%d\
                      and user_id=%d'%(USER_PERMISSION, group_id, user_id)
                work_c.execute(sql)
                log.info('Administrator %s privileges to lift'%\
                                    (mailbox))
            elif status == USER_PERMISSION:
                log.info(" %s is regular user"%mailbox)
            else:
                log.error(" %s isn't %s's member"%\
                                    (mailbox, gname))

def group_op(st, mailbox):
    command = st.pop(0)
    gname = st.pop(0)
    mailbox_list = st[0].split(',')
    if command == 'bind':
        for mailbox in mailbox_list:
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            status = get_status(gname, mailbox)
            if group_id and user_id and not status:
                sql = 'insert into user_group (group_id, user_id, status)\
                        values (%d, %d, %d)'%(group_id, user_id,\
                                              USER_PERMISSION)
                work_c.execute(sql)
                log.info("Binding %s to %s success!"%\
                                    (mailbox,gname))
            else:
                log.warning("%s already is the member of %s."%(mailbox, gname))
    elif command == 'unbind':
        for mailbox in mailbox_list:
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            status = get_status(gname, mailbox)
            if group_id and user_id and status == USER_PERMISSION:
                sql = "delete from user_group where group_id=%d and\
                        user_id=%d;"%(group_id, user_id)
                work_c.execute(sql)
                log.info("Unbinding %s to %s success!"%\
                                    (mailbox,gname))
            else:
                log.warning("%s can't unbind to %s"%\
                                    (mailbox, gname))

def user_op(st, mailbox):
    command = st.pop(0)
    gname = st.pop(0)
    group_id = get_groupid(gname)
    user_id = get_userid(mailbox)
    print command ,gname
    if command == 'unsubscribe':
        sql = "delete from user_group where group_id=%d and user_id=%d"%\
                (group_id, user_id)
        work_c.execute(sql)
        log.info("Success unsubscribe mail from group %s"%gname)
    #elif command == 'update':
    #    sql = "update mg_user set signature=%s where id=%d;"%\
    #                        (signature, user_id)
   #    log.info("Update you signature to %s"%signature)

def help_op(command, st):
    log.info("Error command:%s %s"%(command,st))

def system_mail(rmail):
    payload_dict = parse_mail.parse_email_payload(rmail)
    payload = payload_dict['plain']
    mailbox = re.search(r'[\w\-][\w\-\.]+@[\w\-]+\.[a-zA-Z]{1,4}',
                         rmail['from']).group()

    statement_list = payload.split(';')
    statement_list.pop()# Abandon the '\n\n'
    for statement in statement_list:
        st = statement.lower().split()
        command = st.pop(0)
        group_name = st[1]
        
        if command == 'admin' and admin_permissions(mailbox):
            admin_op(st, mailbox)
        elif command == 'group' and get_status(group_name, mailbox) ==\
                GROUP_PERMISSION:
            group_op(st, mailbox)
        elif command == 'user' and get_status(group_name, mailbox) ==\
                USER_PERMISSION:
            user_op(st, mailbox)
        else:
            help_op(command,st)

    work_c.close() # close the database connection
    file = open('log/temp.log', 'r')
    spayload = file.read()
    file.close()
    smail = MIMEText(spayload, 'plain', 'utf-8')
    subject = "maigroup system receipt"
    smail['Subject'] = generate_mail.encode_header(subject)
    smail['To'] = mailbox
    return smail

if __name__ == '__main__':
    file = open('mg_process.eml', 'r')
    rmail = email.message_from_file(file)
    file.close()
    smail = system_mail(rmail)
    file = open('mg_process_receipt.eml', 'w')
    file.write(smail.as_string())
    file.close()

