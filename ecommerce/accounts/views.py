import re
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserAddressForm
from .models import EmailConfirmed, UserDefaultAddress


# Create your views here.


def logout_view(request):
    """
    Logout View.
    :param request: Http request.
    :return: Redirect to login page.
    """
    logout(request)
    # messages.success(request, 'Successfully logged out. Feel free to <a href="{0}">login</a> again.'
    messages.success(request, "<strong>Successfully</strong> logged out. Feel free to <a href='%s'>login</a> again."
                     % (reverse('auth_login')), extra_tags="safe")
    # messages.debug(request, '%s SQL statements were executed.' % 2)
    # messages.info(request, 'INFO.')
    messages.warning(request, 'WARNING.')
    # messages.error(request, 'ERROR.')

    return HttpResponseRedirect(reverse('auth_login'))


def login_view(request):
    """
    Logout View.
    :param request: Http request.
    :return: Redirect to home page or login form.
    """
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
    """
    Registration View. Allows a user to register an account.
    :param request: Http request.
    :return: Redirect to the home page or registration page.
    """
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
    """
    Activation View. Allows a user to activate their account. Creates a activation key that will be send to the user.
    :param request: Http request.
    :return: Activation complete page or Http404.
    """
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
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


def add_user_address(request):
    print "add_user_address".format(request.GET)
    try:
        next_page = request.GET.get("next")
        print("add_user_address {0}".format(next_page))
    except Exception, e:
        next_page = None
    address_form = UserAddressForm(request.POST or None)
    if request.method == "POST":
        if address_form.is_valid():
            print("add_user_address IN IS VALUE {0}".format(address_form))
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default = address_form.cleaned_data['default']
            if is_default:
                # get or create a default address model - not edit!
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping = new_address
                default_address.save()
            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page)))
    submit_btn = 'Save Address'
    form_title = "Add New Address"
    context = {
        'form': address_form,
        'submit_btn': submit_btn,
        'form_title': form_title,
    }
    return render(request, "form.html", context)





