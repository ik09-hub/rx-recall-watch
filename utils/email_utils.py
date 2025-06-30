import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

email_host = os.getenv("EMAIL_HOST")
email_port = int(os.getenv("EMAIL_PORT", 587))
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
recipient_email = os.getenv("RECIPIENT_EMAIL")

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
            print("Email sent")

    except Exception as e:
        print(f"Failed to send email: {e}")



