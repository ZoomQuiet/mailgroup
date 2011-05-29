# Import smtplib for the actual sending function
import mg_send
import email

# Import the email modules we'll need

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open('test1.eml', 'r')
# Create a text/plain message
smail = email.message_from_file(fp)
fp.close()

s = mg_send.smtp_connection()
s.sendmail('xdwea', smail['To'], smail)
s.quit()
