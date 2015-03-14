from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, RegistrationForm

# Create your views here.


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)

    context = {
        "form": form
    }

    return render(request, "form.html", context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        # first_name = form.cleaned_data['first_name']
        # last_name = form.cleaned_data['last_name']
        new_user.save() #runs form's save method
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request, user)

    context = {
        "form": form
    }

    return render(request, "form.html", context)
