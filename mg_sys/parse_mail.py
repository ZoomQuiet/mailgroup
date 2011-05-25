import email
import email.header
from email.mime.multipart import MIMEMultipart

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


