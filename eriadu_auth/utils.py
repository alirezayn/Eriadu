import requests
import logging


def send_verification_code(mobile, code):
    url = 'https://api.sms.ir/v1/send/verify'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': 'rX4ZsdADrnaDjrdpr8eG4rBW25lElddcvmMGjbIZvbOj2YJQqeSeODq78twjpT2e',
    }
    post_data = {
        'mobile': mobile,
        'templateId': '300543',
        'parameters': [
            {
                'name': 'code',
                'value': code
            }
        ]
    }
    
    try:
        response = requests.post(url, json=post_data, headers=headers)
        print(response.status_code)
        response.raise_for_status()
        response_body = response.text
        logging.info(f'SMS sent successfully: {response_body}')
        return response_body
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to send SMS: {e}')
        return False
