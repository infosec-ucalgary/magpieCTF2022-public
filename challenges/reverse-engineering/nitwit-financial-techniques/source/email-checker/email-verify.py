import email, imaplib, os
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import ssl

# flag
FLAG = "magpie{8uy_5tUp1d_t3CH_m4K3_5TuP1d_m0N3y}"

# email checking regex
regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

#Credentials
USERNAME = 'vexillum.fur'
PASSWORD = '<PASSWORD>'

# Base image for comparison
file_name = "fingerprint.png"
dir_path = os.path.dirname(os.path.abspath(__file__))

fingerprint = (os.path.join(dir_path, file_name))

def getEmailAddress(senderLine):
    address = re.search(regex, senderLine)
    return address.group(0)

def sendEmail(senderEmail, success):
    if success:
        # setup the email message to send them
        port = 465
        email_message = MIMEMultipart("alternative")
        email_message["Subject"] = "Thank You"
        email_message["From"] = "vexillum.fur@gmail.com"
        email_message["To"] = senderEmail
        text = "You did it.  Using this fingerprint we'll be able to flood the market with genuine fake NFT flags.\n\nYour payment, as promised: " + FLAG + "\n\nHappy heisting Flag Hunter,\nVex"
        compiled = MIMEText(text, "plain")
        email_message.attach(compiled)
        # Create a secure SSL context for the gmail account to send the email
        context = ssl.create_default_context()
        # send the verification email from the gmail account
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("vexillum.fur@gmail.com", PASSWORD)
            server.sendmail("vexillum.fur@gmail.com", senderEmail, email_message.as_string())
    else:
        # setup the email message to send them
        port = 465
        email_message = MIMEMultipart("alternative")
        email_message["Subject"] = "Nice Try..."
        email_message["From"] = "vexillum.fur@gmail.com"
        email_message["To"] = senderEmail
        text = "Sorry Flag Hunter, but that fingerprint isn't correct.  Our genuine fakes are being identified by Mom & Pop.\n\nTry again Flag Hunter,\nVex"
        compiled = MIMEText(text, "plain")
        email_message.attach(compiled)
        # Create a secure SSL context for the gmail account to send the email
        context = ssl.create_default_context()
        # send the verification email from the gmail account
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("vexillum.fur@gmail.com", PASSWORD)
            server.sendmail("vexillum.fur@gmail.com", senderEmail, email_message.as_string())

def emptyEmail(senderEmail):
            # setup the email message to send them
        port = 465
        email_message = MIMEMultipart("alternative")
        email_message["Subject"] = "No attachment"
        email_message["From"] = "vexillum.fur@gmail.com"
        email_message["To"] = senderEmail
        text = "Your email has no attachment.  Don't waste your time and mine.  Get that fingerprint and send it when you have it.\n\nGet to work Flag Hunter,\nVex"
        compiled = MIMEText(text, "plain")
        email_message.attach(compiled)
        # Create a secure SSL context for the gmail account to send the email
        context = ssl.create_default_context()
        # send the verification email from the gmail account
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("vexillum.fur@gmail.com", PASSWORD)
            server.sendmail("vexillum.fur@gmail.com", senderEmail, email_message.as_string())

###############################################################################
# Main loop starts here                                                       #
###############################################################################

def main():
    # open the base pattern and get the md5 hash of it
    with open(fingerprint, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()    
        # pipe contents of the file through
        original_md5 = hashlib.md5(data).hexdigest()

    #Create Connection
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(USERNAME, PASSWORD) 

    #Which Gmail Folder to Select?
    mail.select("Inbox")

    # get unread emails
    status, response = mail.search(None, 'UNSEEN')
    unread_msgs = response[0].split()

    for num in response[0].split():
        type, data = mail.fetch(num, '(RFC822)')

        # get the raw data from the mail
        raw_email = data[0][1]

        # get the sender address and email message
        raw_email_string = raw_email.decode('utf-8')
        sender = email.message_from_string(raw_email_string)
        senderEmail = getEmailAddress(sender['from'])
        email_message = email.message_from_string(raw_email_string)

        print(email_message['Content-Type'])

        if "multipart/mixed" not in email_message['Content-Type']:
            emptyEmail(senderEmail)
            continue
        
        # downloading attachments
        for part in email_message.walk():
            # check if the email has an attachment, if not send emptyEmail
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                # can't figure out attachment
                continue

            # get the hash of the file
            file_hash = hashlib.md5(part.get_payload(decode=True)).hexdigest()

            # compare the hash
            if file_hash == original_md5:
                # reply with a thank you and a flag
                sendEmail(senderEmail, True)

            else:
                # reply letting them know it's not genuine, tell them to try again
                sendEmail(senderEmail, False)

if __name__ == "__main__":
    main()