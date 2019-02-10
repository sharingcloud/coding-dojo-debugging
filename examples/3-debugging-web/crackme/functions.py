"""Functions."""

import random
import string

from .models import Profile


def generate_hex():
    """Generate hex."""
    return "".join(
        random.choice(string.ascii_letters) for _ in range(32)
    )


def generate_code(z):
    """Generate code."""
    y = ord('A')
    a = [z[x:x+4] for x in range(29)]
    b = "".join(
        ["".join(
            [chr(((((ord(k) - y) * (ord(k) - y))) % 30) + y) for k in x][::-1]
        ) for x in a]
    )
    c = "-".join([b[x:x+8] for x in range(0, 32, 8)])
    return c


def set_challenge_success(user):
    profile = Profile.objects.get(user=user)
    profile.challenge_success = True
    profile.save()


def set_bonus_success(user):
    profile = Profile.objects.get(user=user)
    profile.bonus_success = True
    profile.save()
