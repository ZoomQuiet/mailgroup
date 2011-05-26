import re
import MySQLdb
import parse_mail
import generate_mail
import api_42qu

global work_c
work_db = MySQLdb.connect(host="127.0.0.1", user="root",\
                          passwd="root", db="mailgroup" charset="utf8")
work_c = work_db.cursor()

GROUP_PERMISSION = 99
USER_PERMISSION = 1

def get_userid(mailbox):
    sql = "select id from mg_user where mailbox='%s';"%mailbox
    if work_c.execute(sql):
        user_id = work_c.fetchone()[0]
        return user_id
    else:
        return False

def get_groupid(gname):
    sql = "select id from mg_group where gname='%s';"%ganme
    if  work_c.execute(sql):
        group_id = work_c.fetchone()[0]
        return group_id
    else:
        return False

def get_status(gname, mailbox):
    user_id = get_userid(mailbox)
    group_id = get_groupid(gname)
    sql = "select status from user_group where gruop_id=%d and user_id=%d"
    if user_id and group_id and work_c.execute(sql%(group_id, user_id)):
        status = work_c.fetchone()[0]
        return status
    else:
        return False
    
#the status user:1, group_admin:99
def admin_permissions(mailbox);
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
    mailbox_list = st.split(',')
    if command == 'create':
        if get_groupid(gname):
            send_content.append('mail group %s already exist'%gname)
        else:
            sql = 'insert into mg_group (gname) values(%s);'%(st[0])
            work_c.execute(sql)
            send_content.append('mail group %s create succee!'%gname)
    elif command == 'bind':
        for mailbox in mailbox_list:
            status = get_status(gname, mailbox)
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            if status == GROUP_PERMISSION:
                send_content.append('group %s exist administator %s'%
                                    (gname, mailbox))
            elif status == USER_PERMISSION:
                sql = 'update user_group set status=%d where group_id=%d\
                      and user_id=%d'%(GROUP_PERMISSION, group_id, user_id)
                send_content.append('Add administrator %s privileges to %s'\
                                    %(mailbox, gname))
            else:
                sql = 'insert into user_group (group_id, user_id, status)\
                        values (%d, %d, %d)'%(group_id, user_id,\
                                              GROUP_PERMISSION)
                work_c.execute(sql)
                send_content.append('group %s add administrator %s '%\
                                    (gname, mailbox))
    elif command == 'del':
        for mailbox in mailbox_list:
            status = get_status(gname, mailbox)
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            if status == GROUP_PERMISSION:
                sql = 'update user_group set status=%d where group_id=%d\
                      and user_id=%d'%(USER_PERMISSION, group_id, user_id)
                send_content.append('Administrator %s privileges to lift'%\
                                    (mailbox))
            elif status == USER_PERMISSION:
                send_content.append(" %s is regular user"%mailbox)
            else:
                send_content.append(" %s isn't %s's member"%\
                                    (mailbox, gname))

def group_op(st, mailbox):
    command = st.pop(0)
    gname = st.pop(0)
    mailbox_list = st.split(',')
    if command == 'bind':
        for mailbox in mailbox_list:
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            status = get_status(gname, mailbox):
            if group_id and user_id and not status:
                sql = 'insert into user_group (group_id, user_id, status)\
                        values (%d, %d, %d)'%(group_id, user_id,\
                                              USER_PERMISSION)
                work_c.execute(sql)
                send_content.append("Binding %s to %s success!"%\
                                    (mailbox,gname))
            else:
                send_content.append("%s cann't bind to %s"%(mailbox, gname))
    elif command == 'del':
        for mailbox in mailbox_list:
            group_id = get_groupid(gname)
            user_id = get_userid(mailbox)
            status = get_status(gname, mailbox):
            if group_id and user_id and status == USER_PERMISSION:
                sql = "delete from user_group where group_id=%d and\
                        user_id=%d;"%(group_id, user_id)
                work_c.execute(sql)
                send_content.append("Unbinding %s to %s success!"%\
                                    (mailbox,gname))
            else:
                send_content.append("%s cann't unbind to %s"%\
                                    (mailbox, gname))

def user_op(st, mailbox):
    command = st.pop(0)
    gname = st.pop(0)
    group_id = get_groupid(gname)
    user_id = get_userid(mailbox)
    if command == 'unsubscribe':
        sql = "delete from user_group where group_id=%d and user_id=%d"%\
                (group_id, user_id)
        send_content.append("Success unsubscribe mail from group %s"%gname)
    #elif command == 'update':
    #    sql = "update mg_user set signature=%s where id=%d;"%\
    #                        (signature, user_id)
   #    send_content.append("Update you signature to %s"%signature)

def help_op():
    send_content.append("TODO: attach help file")

def system_mail(rmail):
    global send_content
    send_content = []
    payload_dict = parse_mail.parse_email_payload(rmail)
    payload = payload_dict['plain']
    mailbox = re.search(r'[\w\-][\w\-\.]+@[\w\-]+\.[a-zA-Z]{1,4}',
                         rmail['from']).group()

    statement_list = payload.split(';')
    for statement in statement_list:
        st = statement.lower().split()
        command = st.pop(0)
        group_name = st[0]
        
        if command == 'admin' and admin_permissions(mailbox):
            admin_op(st, mailbox)
        elif command == 'group' and get_status(group_name, mailbox) ==\
                GROUP_PERMISSION:
            group_op(st, mailbox)
        elif command == 'user' and get_status(group_name, mailbox) ==\
                USER_PERMISSION:
            user_op(st, mailbox)
        else:
            help_op()

    spayload = "\n".join(send_content)
    smail = MIMEText(spayload, 'plain', 'utf-8')
    subject = "maigroup system receipt"
    smail['Subject'] = generate_mail.encode_header(subject)
    smail['To'] = mailbox
    return smail






