import http.client
import json
import logging


def send_verification_code(mobile, code):
    conn = http.client.HTTPSConnection("api.sms.ir")
    
    payload = json.dumps({
        "mobile": mobile,
        "templateId": 300543,  # Replace this with your actual template ID
        "parameters": [
            {
                "name": "code",
                "value": code
            }
        ]
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': 'rX4ZsdADrnaDjrdpr8eG4rBW25lElddcvmMGjbIZvbOj2YJQqeSeODq78twjpT2e'  # Replace with your actual API key
    }
    
    try:
        conn.request("POST", "/v1/send/verify", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response_body = data.decode("utf-8")
        logging.info(f'SMS sent successfully: {response_body}')
        return response_body
    except Exception as e:
        logging.error(f'Failed to send SMS: {e}')
        return False
