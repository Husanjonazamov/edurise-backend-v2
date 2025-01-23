import random
from datetime import timedelta
from django.utils import timezone

OTP_VALID_TIME = 5

def generate_otp():
    return 123456
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def is_otp_time_valid(code_creation_time):
    otp_validity_period = timedelta(minutes=OTP_VALID_TIME)
    otp_expiration = code_creation_time + otp_validity_period

    return timezone.now() <= otp_expiration