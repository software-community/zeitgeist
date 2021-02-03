from TSP.models import Payment
from instamojo_wrapper import Instamojo
import os
import requests

from django.urls import reverse


def payment_request(name, amount, purpose, email, mobile):
    api = Instamojo(api_key=os.getenv('API_AUTH_KEY'),
                    auth_token=os.getenv('API_AUTH_TOKEN'))

    # Create a new Payment Request
    response = api.payment_request_create(
        buyer_name=name,
        amount=amount,
        purpose=purpose,
        send_email=True,
        email=email,
        phone=mobile,
        redirect_url="https://zeitgeist.org.in/TSP/payment_redirect/",
        webhook="https://zeitgeist.org.in/TSP/webhook/"
    )
    return response

def get_paid_details(profile):

    payments = Payment.objects.filter(profile=profile)

    num_cat_a = 0
    num_cat_b = 0

    for payment in payments:
        if payment.transaction_id != 'none' and payment.transaction_id != '0':
            num_cat_a = num_cat_a + payment.category_a
            num_cat_b = num_cat_b + payment.category_b

    return num_cat_a, num_cat_b
