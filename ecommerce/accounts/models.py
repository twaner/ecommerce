from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

# from localflavor.us.models import PhoneNumberField
from localflavor.us.us_states import US_STATES
# Create your models here.


class UserStripe(models.Model):
    # Each user has one Stripe ID; fk would allow for multiple
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        activation_url = "{0}{1}" \
                         .format(settings.SITE_URL, reverse("activation_view", args=[self.activation_key]))
        context = {
            "activation_key": self.activation_key,
            "activation_url": activation_url,
            "user": self.user.username,
        }
        message = render_to_string("accounts/activation_message.txt", context)
        subject = "Activate your email"
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)


class EmailMarketingSignup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# NEW_STATE = (
#     ("AB", "ABC STATE"),
#     ("BC", "BC STATE"),
#     )

class UserAddressManager(models.Manager):
    def get_billing_addresses(self, user):
        return super(UserAddressManager, self).filter(user=user).filter(billing=True)
        # if billing:
        #     address = "{0} {1}".format(self.address, self.address2)
        #     return "{0}, {1}, {2}, {3}, {4}".format(address, self.city, self.state, self.country, self.zipcode)
        # else:
        #     return ""

NEW_STATE = US_STATES

class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    shipping = models.ForeignKey("UserAddress", null=True, blank=True,\
     related_name='user_address_shipping_default')
    billing = models.ForeignKey("UserAddress", null=True, blank=True,\
     related_name='user_address_billing_default')

    class Meta:
        verbose_name = "UserDefaultAddress"
        verbose_name_plural = "UserDefaultAddresses"
    
    def __str__(self):
        return "{0}".format(str(self.user.username))    
    

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, choices=NEW_STATE, null=True, blank=True)
    country = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120, null=True, blank=True)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = UserAddressManager()

    class Meta:
        verbose_name = "UserAddress"
        verbose_name_plural = "UserAddresss"

    def __str__(self):
        return str(self.user.username)

    def get_address(self):
        address = "{0} {1}".format(self.address, self.address2)
        return "{0}, {1}, {2}, {3}, {4}".format(address, self.city, self.state, self.country, self.zipcode)

    
    

