import smtplib
from email.message import EmailMessage
import random

def send_otp(email: str):

    sender = "lakhya.arnav.cs.project@gmail.com"

    otp = random.randint(100000, 999999)
    message = EmailMessage()
    message.set_content(f'The OTP for Alpha Bravo password reset is: {otp}')
    
    message['Subject'] = f'Alpha-Bravo Password Recovery [{otp}]'
    message['From'] = sender
    message['To'] = email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, "tkbw uufq ziyx smnq")
    

    server.send_message(message)
    server.quit()

    return otp