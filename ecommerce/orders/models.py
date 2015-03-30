from decimal import Decimal
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
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

try:
    tax_rate = settings.DEFAULT_TAX_RATE
except Exception, e:
    print(str(e))
    raise NotImplementedError(str(e))

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

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-updated"]

    def __str__(self):
        return self.order_id

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        two_places = Decimal(10) ** -2
        tax_rate_dec = Decimal("0".format(tax_rate))
        sub_total_dec = Decimal(self.sub_total)
        tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
        instance.tax_total = tax_total_dec
        instance.final_price = sub_total_dec + tax_rate_dec
        instance.save()
        return instance.final_price