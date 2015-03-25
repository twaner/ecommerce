import datetime
import json
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.shortcuts import render, HttpResponse, Http404
from .forms import EmailForm
from accounts.models import EmailMarketingSignup

# Create your views here.


def dismiss_marketing_message(request):
    if request.is_ajax():
        data = {"success": True}
        json_data = json.dumps(data)
        request.session['dismiss_message_for'] = str(timezone.now() +
                                                     datetime.timedelta(hours=settings.MARKETING_HOURS_OFFSET,
                                                                        seconds=settings.MARKETING_SECONDS_OFFSET))
        return HttpResponse(json_data, content_type="application/json")
    else:
        raise Http404
        # TODO return something else

def email_signup(request):
    if request.method == "POST":
        print "email_signup request.POST --> {0}".format(request.POST)
        form = EmailForm(request.POST)
        if form.is_valid():
            email =  form.cleaned_data['email']
            new_signup = EmailMarketingSignup.objects.create(email=email)
            request.session['email_added_marketing'] = True
            return HttpResponse("Success - {0}".format(email))
        if form.errors:
            print "email_signup form.errors --> {0}".format(form.errors)
            json_data = json.dumps(form.errors)
            request.session['email_added_marketing'] = False
            return HttpResponseBadRequest(json_data, content_type="application/json")
    else:
        raise Http404