import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymysql.cursors
from backend.Utils.user_utils import get_username
from backend.mail_former import otp_2, otp_1, delete_1, delete_2, perm_delete_1, perm_delete_2

passwd = 'tkbw uufq ziyx smnq'
sender = "lakhya.arnav.cs.project@gmail.com"


def send_otp(email: str) -> int:
    """
    Sends a random 6-digit `OTP` to `email`
    Returns `OTP` if `email` is valid, else returns `-1`
    """

    try:

        otp = random.randint(100000, 999999)
        message = MIMEMultipart("alternative")

        message['Subject'] = f'Cinematch OTP'
        message['From'] = sender
        message['To'] = email

        # write the text/plain part
        text = """
        OTP
        """

        # write the HTML part
        html = otp_1 + f"{otp}" + otp_2

        # convert both parts to MIMEText objects and add them to the MIMEMultipart message
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, passwd)

        server.send_message(message)
        server.quit()

        return otp

    except:
        return -1


def send_deletion_mail(email: str, cursor: pymysql.cursors.Cursor) -> bool:
    """
    Sends a mail to inform about the deletion of the user's account
    """
    try:
        username = get_username(email, cursor)

        message = MIMEMultipart("alternative")

        message['Subject'] = f'Cinematch Account Deletion'
        message['From'] = sender
        message['To'] = email

        text = """
        Deletion
        """

        html = delete_1 + f"{username}" + delete_2

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, passwd)

        server.send_message(message)
        server.quit()

        return True

    except:
        return False


def send_removal_mail(username: str, email: str) -> bool:
    """
    Sends a mail to inform about the removal of the user's account
    """
    try:
        if username:
            message = MIMEMultipart("alternative")

            message['Subject'] = f'Cinematch Account Removal'
            message['From'] = sender
            message['To'] = email

            # write the text/plain part
            text = """
            Delete Account Permanent
            """

            # write the HTML part
            html = perm_delete_1 + f"{username}" + perm_delete_2

            # convert both parts to MIMEText objects and add them to the MIMEMultipart message
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, passwd)

            server.send_message(message)
            server.quit()

            return True

        return False

    except:
        return False
