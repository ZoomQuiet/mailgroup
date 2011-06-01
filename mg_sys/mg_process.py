import re
import email
from email.mime.text import MIMEText
import api_42qu
import mg_log
from mg_util import connection, get_userid, get_groupid, get_status
from mg_util import USER_PERMISSION, GROUP_PERMISSION, admin_permission
from mg_util import parse_email_payload, encode_header

log = mg_log.tempLogger()
    
global work_c
work_c = connection()

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
            user_id = get_userid(mailbox, True)
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
            user_id = get_userid(mailbox, True)
            status = get_status(gname, mailbox)
            if group_id and user_id and not status:
                sql = 'insert into user_group (group_id, user_id, status)\
                        values (%d, %d, %d)'%(group_id, user_id,\
                                              USER_PERMISSION)
                work_c.execute(sql)
                log.info("Binding %s to %s success!"%\
                                    (mailbox,gname))
            else:
                if user_id:
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
    payload_dict = parse_email_payload(rmail)
    payload = payload_dict['plain']
    mailbox = re.search(r'[\w\-][\w\-\.]+@[\w\-]+\.[a-zA-Z]{1,4}',
                         rmail['from']).group()

    statement_list = payload.split(';')
    statement_list.pop()# Abandon the '\n\n'
    for statement in statement_list:
        st = statement.lower().split()
        command = st.pop(0)
        group_name = st[1]
        
        if command == 'admin' and admin_permission(mailbox):
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
    smail['Subject'] = encode_header(subject)
    smail['To'] = mailbox
    smail['X-Group'] = str(0) #The system mail group is 0
    smail['X-Topic'] = str(0) #The system mail topic is 0
    return smail

if __name__ == '__main__':
    file = open('test/mg_process.eml', 'r')
    rmail = email.message_from_file(file)
    file.close()
    smail = system_mail(rmail)
    file = open('test/mg_process_receipt.eml', 'w')
    file.write(smail.as_string())
    file.close()

