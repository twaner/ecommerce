from django.db import models
from django.conf import settings

# Create your models here.


class UserStripe(models.Model):
    # Each user has one Stripe ID; fk would allow for multiple
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=120)

    def __str__(self):
        return str(self.stripe_id)


