import email.header
from email.mime.text import MIMEText

def attach_payload(payload_dict, smail):
    """Encode and attach the payload

    Example

    Args:
        payload_dict: the dict of payload
        smail: the email object for construct

    Return: 
        the email.message object

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
