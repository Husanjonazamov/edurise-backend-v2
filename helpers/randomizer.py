import random
import secrets
import string


def generate_random_password(length=12):
    """Generate a random password of a given length."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_random_username(user, length):
    """Generate a random username with the given length."""
    while True:
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

        if not user.objects.filter(username=username).exists():
            return username
