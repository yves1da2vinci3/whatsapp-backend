import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

MY_ADDRESS = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_PASSWORD")

def send_email(email: str, subject: str, message: str):
    try:
        # Create a secure SSL context
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()  # Can be omitted
        server.starttls()
        server.ehlo()  # Can be omitted
        server.login(MY_ADDRESS, PASSWORD)

        # Create a MIMEText object
        msg = MIMEMultipart()
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.send_message(msg)

        print("Email sent successfully")
    except Exception as e:
        print(f"An error occurred while sending email: {str(e)}")
    finally:
        server.quit()
