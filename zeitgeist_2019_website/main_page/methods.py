from instamojo_wrapper import Instamojo
import os

def payment_request(amount, purpose, email):
    api = Instamojo(api_key=os.getenv('api_auth_key'),
                    auth_token=os.getenv('api_auth_token'))

    # Create a new Payment Request
    response = api.payment_request_create(
        amount=amount,
        purpose=purpose,
        send_email=True,
        email=email,
        redirect_url="http://www.example.com/handle_redirect.py",
        webhook="http://www.example.com/handle_redirect.py"
        )
    print(response)
    return response['payment_request']['longurl'], response['payment_request']['id']