from django.contrib import admin
from .models import RegistrationDetails

# Register your models here.

class RegistrationDetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RegistrationDetails._meta.get_fields()]

admin.site.register(RegistrationDetails, RegistrationDetailsAdmin)
