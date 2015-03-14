from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from carts.models import Cart

# User
# try:
#     user = get_user_model()
# except ImportError:
#     from django.contrib.auth.models import User
#     user = get_user_model()
# Choices

STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)

# Create your models here.


class Order(models.Model):
    # TODO address
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    order_id = models.CharField(max_length=120, default="ABC", unique=True)
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    sub_total = models.DecimalField(default=1.99, decimal_places=2, max_digits=10)
    tax_total = models.DecimalField(default=1.99, decimal_places=2, max_digits=10)
    final_price = models.DecimalField(default=1.99, decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.order_id