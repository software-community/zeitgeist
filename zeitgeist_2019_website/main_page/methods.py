from instamojo_wrapper import Instamojo
import os
import requests


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
        redirect_url="https://zeitgeist.org.in/payment_redirect/",
        webhook="https://zeitgeist.org.in/webhook/"
    )
    return response




def support_payment_request(name, amount, purpose, email, mobile):
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
        redirect_url="https://zeitgeist.org.in/support_payment_redirect/",
        webhook="https://zeitgeist.org.in/support_weebhook/"
    )
    return response


def sendNotification(title, message):
    headers = {'Content-type': 'application/json',
               'Authorization': 'key=' + os.environ.get('FCM_APIKEY', '')}
    postdata = {
        
            "notification":
            {
                "body": message,
                "title": title
            },
            "priority": "high",
            "data":
            {
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            },
            "condition": "!('anytopicyoudontwanttouse' in topics)"
        
    }
    r = requests.post('https://fcm.googleapis.com/fcm/send', json = postdata, headers = headers)
    print(r.text)
