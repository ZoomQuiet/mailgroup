import email
import os
import os.path
import mg_receive
import mg_log

log = mg_log.receiveLogger()

path = os.path.normpath(os.path.join(os.getcwd(), __file__))
os.chdir(os.path.split(path)[0])
os.chdir('../mail_source/download')

def download_mail():
    imap = mg_receive.imap_connection()
    status, data = imap.select('INBOX')
    status, data = imap.search('utf8', '(seen)')
    if data[0]:
        mail_list = data[0].split()
        for mail_no in mail_list:
            status, data = imap.fetch(mail_no, 'rfc822')
            mail = email.message_from_string(data[0][1])
            filename = '%s'%mail['message-id']
            log.info('down %s %s'%(mail_no, filename))
            file = open(filename, 'w')
            file.write(data[0][1])
            file.close()
    else:
        print 'no mail'

if __name__ == '__main__':
    download_mail()
