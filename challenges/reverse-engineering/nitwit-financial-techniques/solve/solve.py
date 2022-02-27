import email, imaplib, os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import ssl
from email import encoders
from prometheus_client import start_http_server, Gauge

# flag
FLAG = "magpie{8uy_5tUp1d_t3CH_m4K3_5TuP1d_m0N3y}"

#Credentials
USERNAME = '2021magpie.inc'
PASSWORD = '<PASSWORD>'

FAIL_G = Gauge("Nitwit_Financial_Techniques_fails",
    "number of failures of challenge nitwit_financial_techniques")

# time to wait between send and check receive
WAIT_TIME = 60

# connect to email
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(USERNAME, PASSWORD)

def solve() -> bool:

    # Base image for comparison
    file_name = "fingerprint.png"
    dir_path = os.path.dirname(os.path.abspath(__file__))

    fingerprint = (os.path.join(dir_path, file_name))

    # send an email to vex with the fingerprint
    port = 465
    email_message = MIMEMultipart("mixed")
    email_message["Subject"] = "TEST SOLVE"
    email_message["From"] = "2021magpie.inc@gmail.com"
    email_message["To"] = "vexillum.fur@gmail.com"
    # add the text body
    text = "THIS IS A SOLVE TEST"
    compiled = MIMEText(text, "plain")
    email_message.attach(compiled)

    # Open the fingerprint
    with open(fingerprint, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_name}",
    )

    # Add attachment to message and convert message to string
    email_message.attach(part)

    # Create a secure SSL context for the gmail account to send the email
    context = ssl.create_default_context()

    # send the verification email from the gmail account
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("2021magpie.inc@gmail.com", PASSWORD)
        server.sendmail("2021magpie.inc@gmail.com", "vexillum.fur@gmail.com", email_message.as_string())

    # wait 2 minutes
    time.sleep(WAIT_TIME)

    # get any unread emails and check for the flag
    # select the inbox
    mail.select("Inbox")

    # get unread messages
    status, response = mail.search(None, 'UNSEEN')

    for num in response[0].split():
        type, data = mail.fetch(num, '(RFC822)')

        # get the raw data from the mail
        raw_email = data[0][1]

        # if flags match, return true
        if FLAG in raw_email.decode('utf-8'):
            return True
    
    # return false if cycled through all the emails and none had the flag
    return False

if __name__ == "__main__":
    start_http_server(12311)

    while True:
        if solve():
            FAIL_G.set(0)
        else:
            FAIL_G.inc()