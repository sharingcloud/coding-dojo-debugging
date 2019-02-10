"""Models."""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_data = models.CharField(max_length=255, default='')
    challenge_success = models.BooleanField(default=False)
    bonus_success = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"[{self.user}] Challenge: {self.challenge_success} "
            f"/ Bonus: {self.bonus_success}"
        )
