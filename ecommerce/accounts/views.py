import re
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import EmailConfirmed

# Create your views here.


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out. Feel free to log in again.")
    return HttpResponseRedirect(reverse('auth_login'))


def login_view(request):
    form = LoginForm(request.POST or None)
    submit_btn = "Login"
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully logged in. Welcome back!")
        return HttpResponseRedirect("/")

        # user.emailconfirmed.activate_user_email()

    context = {
        "form": form,
        "submit_btn": submit_btn
    }

    return render(request, "form.html", context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    submit_btn = "Join"
    if form.is_valid():
        new_user = form.save(commit=False)
        # first_name = form.cleaned_data['first_name']
        # last_name = form.cleaned_data['last_name']
        new_user.save()  # runs form's save method
        messages.success(request, "Successfully register. Please confirm your email now.")
        return HttpResponseRedirect("/")
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request, user)

    context = {
        "form": form,
        "submit_btn": submit_btn
    }

    return render(request, "form.html", context)

SHA1_RE = re.compile('^[a-f0-9]{40}$')


def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
            print("instance = EmailConfirmed.objects.get(activation_key=activation_key)")
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "There was an error with your request.")
            raise HttpResponseRedirect("/")
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation successful, welcome!"
            instance.confirmed = True
            instance.activation_key = "Confirmed"
            instance.save()
            messages.success(request, "Successfully confirmed. Please login.")
        elif instance is not None and instance.confirmed:
            page_message = "Already confirmed"
            messages.success(request, "Already confirmed.")
        else:
            page_message = ""
        context = {"page_message": page_message}
        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404