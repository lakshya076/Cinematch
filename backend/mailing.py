import smtplib
from email.message import EmailMessage
import random
import pymysql.cursors
from Utils.user_utils import valid_email, get_username


passwd = 'tkbw uufq ziyx smnq'
sender = "lakhya.arnav.cs.project@gmail.com"

def send_otp(email: str):

    '''
    
    Sends a random 6-digit `OTP` to `email`

    Returns `OTP` if `email` is valid, else returns `-1`
    
    '''

    if valid_email(email):

        otp = random.randint(100000, 999999)
        message = EmailMessage()
        message.set_content(f'The OTP for Cinematch password reset is: {otp}')
        
        message['Subject'] = f'Cinematch Password Recovery'
        message['From'] = sender
        message['To'] = email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, passwd)
        

        server.send_message(message)
        server.quit()

        return otp

    else:
        return -1
    

def send_deletion_mail(email: str, cursor: pymysql.cursors.Cursor):

    if valid_email(email):

        username = get_username(email, cursor)

        message = EmailMessage()

        message_content = f'Dear {username},\n\nYour Cinematch account has been deleted, and will be removed from the database after 30 days.\nIf you want to recover your account, visit our application.'
        message.set_content(message_content)
        
        message['Subject'] = f'Cinematch Account Deletion'
        message['From'] = sender
        message['To'] = email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, passwd)
        
        server.send_message(message)
        server.quit()

        return True

    else:
        return False
    

def send_removal_mail(email: str, cursor: pymysql.cursors.Cursor):

    if valid_email(email):

        username = get_username(email, cursor)

        if username:

            message = EmailMessage()

            message_content = f'Dear {username},\n\nYour Cinematch account has been removed and cannot be recovered from our database.'
            message.set_content(message_content)
            
            message['Subject'] = f'Cinematch Account Removal'
            message['From'] = sender
            message['To'] = email

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, passwd)
            
            server.send_message(message)
            server.quit()

            return True

        return False

    else:
        return False