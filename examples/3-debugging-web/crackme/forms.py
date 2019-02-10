"""Forms."""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """Login form."""

    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        try:
            # Check if user exists
            User.objects.get(username=username)

            # Try to authenticate
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError(f"Bad password for username {username}")

            self.cleaned_data["existing"] = True
            self.cleaned_data["user"] = user

        except User.DoesNotExist:
            self.cleaned_data["existing"] = False

        return self.cleaned_data
