from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, EmailMarketingSignup, UserAddress

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)

class EmailMarketingSignupAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'timestamp']

	class Meta:
		model = EmailMarketingSignup

admin.site.register(EmailMarketingSignup, EmailMarketingSignupAdmin)

class UserAddressAdmin(admin.ModelAdmin):

    class Meta:
        model = UserAddress

admin.site.register(UserAddress, UserAddressAdmin)
