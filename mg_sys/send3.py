# Import smtplib for the actual sending function
import smtplib
import mg_send

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open('../readme', 'rb')
# Create a text/plain message
msg = MIMEText(fp.read(),'plain','utf-8')
fp.close()

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % 'textfilei'
msg['From'] = 'silegon'
msg['To'] = 'silegon@gmail.com'

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = mg_send.smtp_connection()
s.sendmail('xdwea', 'silegon@gmail.com', msg.as_string())
s.quit()
