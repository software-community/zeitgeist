from django.contrib import admin
from .models import RegistrationDetails

# Register your models here.

class RegistrationDetailsAdmin(admin.ModelAdmin):

    list_display = ['get_user_name', 'get_user_email', 'campus_ambassador_code', 'college', 'mobile_number']

    def get_user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    get_user_name.short_description = 'User Name'
    get_user_name.admin_order_field = 'user__first_name'

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = 'User Email'
    get_user_email.admin_order_field = 'user__email'

admin.site.register(RegistrationDetails, RegistrationDetailsAdmin)
