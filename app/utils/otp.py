import random
from .mail import send_email
from .redis_client import set_otp


async def send_otp(email: str):
    new_otp = random.randint(100000, 999999)
    await send_email(email, "OTP", f"Your OTP is {new_otp}")
    await set_otp(email, new_otp)
    print(f"Sending OTP to {email}")
