import imaplib
import email
import ConfigParser
import os
import os.path
import mg_log

log = mg_log.sysLogger()

def imap_connection():
    config = ConfigParser.RawConfigParser()
    
    path = os.path.normpath(os.path.join(os.getcwd(), __file__))
    config.read(os.path.split(path)[0] + '/local_email.cfg')

    imap_server = config.get('receive_mail', 'imap_server')
    imap_server_port = config.getint('receive_mail', 'imap_server_port')
    username = config.get('receive_mail', 'username')
    password = config.get('receive_mail', 'password')

    #print imap_server, imap_server_port
    imapserver = imaplib.IMAP4_SSL(imap_server, imap_server_port)
    #print username, password
    type, data = imapserver.login(username, password)
    if type == 'OK':

        #log.info('imap:'+ data[0])
        log.info('imap loging success')
    else:
        log.error('imap:'+ data[0])
        
    return imapserver

imap = None
def get_new_mail():
    global imap
    if imap == None:
        imap = imap_connection() 
        imap.select('inbox')
    imap.check()
    type, data = imap.search('utf-8','(unseen)')
    if type == 'OK':
        if len(data) > 0:
            mail_source = []
            mail_list = data[0].split()
            for mail_no in mail_list:
                status, data = imap.fetch(mail_no, 'rfc822')
                mail = email.message_from_string(data[0][1])
                mail_source.append(mail)
            return mail_source
        else:
            return False

    else:
        log.error('imap: get_new_mail error')

    
    
    

