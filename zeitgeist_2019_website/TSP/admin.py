from django.contrib import admin
from django.contrib import messages
from TSP.models import Profile, Payment, TSPResult

from .utils import check_payment

class ProfileDetails(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

admin.site.register(Profile, ProfileDetails)

class PaymentDetails(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]
    actions = ['refresh_payment']
    
    def refresh_payment(self, request, queryset):
        updated = 0
        msg = ''
        for payment in queryset:
            if payment.transaction_id == '0':
                transaction_id = check_payment(payment.payment_request_id, False)
                if transaction_id and transaction_id.startswith('MOJO'):
                    updated = updated + 1
                    msg = msg + '\n' + str(payment.profile) + '\t' + transaction_id
                    payment.transaction_id = transaction_id
                    payment.save()
        messages.add_message(request, messages.INFO, str(updated) + ' Payments Updated' + msg)

admin.site.register(Payment, PaymentDetails)

class TSPResultAdminView(admin.ModelAdmin):
    list_display = [field.name for field in TSPResult._meta.fields]

admin.site.register(TSPResult, TSPResultAdminView)