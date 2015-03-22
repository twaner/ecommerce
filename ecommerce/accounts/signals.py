__author__ = 'taiowawaner'
import stripe
import random
import hashlib
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from django.db.models.signals import post_save
from .models import UserStripe, EmailConfirmed


stripe.api_key = settings.STRIPE_SECRET_KEY

# Utils


def get_or_create_stripe_user(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
            email=str(user.email)
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()


def user_created(sender, instance, created, *args, **kwargs):
    """
    Signal for when a user is created.
    :param sender: django.contrib.auth.models.User
    :param instance: User.
    :param created: Boolean for if a user was created.
    :param args: args.
    :param kwargs: kwargs
    """
    print "----IN USER created"
    user = instance
    if created:
        print "------IN IF USER created"
        get_or_create_stripe_user(user)
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            print "------IN IF EMail is created"
            short_hash = hashlib.sha1(str(random.random())).hexdigest()[:10]
            base, domain = str(user.email).split("@")
            activation_key = hashlib.sha1(short_hash + base).hexdigest()
            email_confirmed.activation_key = activation_key
            email_confirmed.save()
            email_confirmed.activate_user_email()
            

post_save.connect(user_created, sender=settings.AUTH_USER_MODEL)


# Signals

# If we decide to change how we want to add the stripe id, this is where that would be made for user_logged_in
# def get_or_create_stripe(sender, user, *args, **kwargs):
#     """
#     Signal function to ensure a user has a Stripe ID
#     :param sender: django.contrib.auth.models.User
#     :param user: User who is logged in.
#     :param args: args.
#     :param kwargs: kwargs.
#     """
#     try:
#         user.userstripe.stripe_id
#     except UserStripe.DoesNotExist:
#         customer = stripe.Customer.create(
#             email=str(user.email)
#         )
#         new_user_stripes = UserStripe.objects.create(user=user, stripe_id=customer.id)
#     except:
#         pass
#
# user_logged_in.connect(get_or_create_stripe)


'''
import traceback
import sys
except Exception, err:
        print traceback.format_exc()

'''
