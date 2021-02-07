import requests
import os

def sendNotification(title, message):
    headers = {'Content-type': 'application/json',
               'Authorization': 'key=' + os.environ.get('FCM_KEY', '')}
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


from instamojo_wrapper import Instamojo
def check_payment(request_id, at_sudhir):
    if at_sudhir:
        api = Instamojo(api_key=os.getenv('WORKSHOP_API_AUTH_KEY'),
                        auth_token=os.getenv('WORKSHOP_API_AUTH_TOKEN'))
    else:
        api = Instamojo(api_key=os.getenv('API_AUTH_KEY'),
                    auth_token=os.getenv('API_AUTH_TOKEN'))

    # Create a new Payment Request
    response = api.payment_request_status(request_id)
    if response['success'] and response['payment_request']['status'] == 'Completed':
        for payment in response['payment_request']['payments']:
            if payment['status'] == 'Credit':
                return payment['payment_id']
    return None