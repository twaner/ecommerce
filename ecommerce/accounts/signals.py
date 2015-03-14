__author__ = 'taiowawaner'
import stripe
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from .models import UserStripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Signals

def get_or_create_stripe(sender, user, *args, **kwargs):
    """
    Signal function to ensure a user has a Stripe ID
    :param sender: django.contrib.auth.models.User
    :param user: User who is logged in.
    :param args: args.
    :param kwargs: kwargs.
    """
    try:
        user.userstripe.stripe_id
    except UserStripe.DoesNotExist:
        customer = stripe.Customer.create(
            email=str(user.email)
        )
        new_user_stripes = UserStripe.objects.create(user=user, stripe_id=customer.id)
    except:
        pass


user_logged_in.connect(get_or_create_stripe)

'''
import traceback
import sys
except Exception, err:
        print traceback.format_exc()

'''
