import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
MY_ADDRESS = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_PASSWORD")
s = smtplib.SMTP("smtp.gmail.com", port=587)

def send_email(email: str, subject: str, message: str):
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    email_message = f"Subject: {subject}\n\n{message}"
    s.sendmail("&&&&&&&&&&&", email, email_message)
