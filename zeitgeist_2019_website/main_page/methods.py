from instamojo_wrapper import Instamojo
import os

def payment_request(name,amount, purpose, email,mobile):
    api = Instamojo(api_key=os.getenv('api_auth_key'),
                    auth_token=os.getenv('api_auth_token'))

    # Create a new Payment Request
    response = api.payment_request_create(
        buyer_name=name,
        amount=amount,
        purpose=purpose,
        send_email=True,
        email=email,
        phone=mobile,
        redirect_url="http://zeitgeist.org.in/payment_redirect/",
        webhook="http://zeitgeist.org.in/webhook/"
        )
    return response
    
def accomodation_payment_request(name,amount,purpose,email,mobile):
    api= Instamojo(api_key=os.getenv('api_auth_key'),auth_token=os.getenv('api_auth_token'))

    response = api.payment_request_create(
        buyer_name=name,
        amount=amount,
        purpose=purpose,
        send_email=True,
        email=email,
        phone=mobile,
        redirect_url='http://zeitgeist.org.in/accomodation_payment_redirect/',
        weebhook='http://zeitgeist.org.in/accomodation_weebhook/'
        )
    return response