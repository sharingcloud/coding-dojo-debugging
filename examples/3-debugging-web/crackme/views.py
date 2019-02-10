"""Views."""

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .decorators import bonus_decorator
from .forms import LoginForm
from .functions import (
    generate_hex, generate_code, set_bonus_success, set_challenge_success
)
from .models import Profile


def login(request):
    errors = {}

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = form.cleaned_data.get("user")
            if user is None:
                user = User()
                user.username = username
                user.set_password(password)
                user.save()

                profile = Profile()
                profile.user = user
                profile.save()

            auth_login(request, user)
            return redirect("/challenge")

        else:
            errors = form.errors

    context = {
        "errors": errors
    }

    return render(request, 'crackme/login.html', context)


@require_GET
def logout(request):
    auth_logout(request)
    return redirect("/login")


@login_required
@require_GET
def challenge(request):
    request.session["generated_hex"] = generate_hex()

    return render(request, 'crackme/challenge.html')


@login_required
@require_POST
def check_code(request):
    hexcode = request.session.get("generated_hex")
    passcode = request.POST.get("code")

    if hexcode is not None and generate_code(hexcode) == passcode:
        request.session["passcode"] = passcode
        return HttpResponse(status=204)

    return JsonResponse({"error": "bad code"}, status=400)


@login_required
@require_GET
def secure(request):
    hexcode = request.session.get("generated_hex")
    passcode = request.session.get("passcode")

    if hexcode is not None and generate_code(hexcode) == passcode:
        set_challenge_success(request.user)
        return render(request, 'crackme/secure.html')

    return render(request, 'crackme/secure_fail.html')


@login_required
@require_GET
@bonus_decorator
def bonus(request):
    set_bonus_success(request.user)
    return render(request, 'crackme/bonus.html')
