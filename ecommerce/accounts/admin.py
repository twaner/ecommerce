from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, EmailMarketingSignup

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)

class EmailMarketingSignupAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'timestamp']

	class Meta:
		model = EmailMarketingSignup

admin.site.register(EmailMarketingSignup, EmailMarketingSignupAdmin)