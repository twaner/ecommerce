from django.contrib import admin

# Register your models here.

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "user", "status", "sub_total", "tax_total", "final_price", "updated"]

    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
