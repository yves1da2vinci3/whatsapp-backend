import random
from .mail import send_email
from .redis_client import set_otp


def send_otp(email: str):
    new_otp = random.randint(100000, 999999)
    send_email(email, "OTP", f"Your OTP is {new_otp}")
    set_otp(email, new_otp)
    print(f"Sending OTP to {email}")
