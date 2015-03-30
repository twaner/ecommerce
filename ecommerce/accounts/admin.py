from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, EmailMarketingSignup, UserAddress, UserDefaultAddress

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)


class EmailMarketingSignupAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp']

    class Meta:
        model = EmailMarketingSignup


admin.site.register(EmailMarketingSignup, EmailMarketingSignupAdmin)


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_address']

    class Meta:
        model = UserAddress


admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserDefaultAddress)