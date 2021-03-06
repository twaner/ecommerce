from django.contrib import admin

# Register your models here.

from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'line_total']

    class Meta:
        model = CartItem


admin.site.register(CartItem, CartItemAdmin)