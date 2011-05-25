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
