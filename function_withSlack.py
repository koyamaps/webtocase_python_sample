"""
# Enviroment Variables List
- ReCAPTCHA_SECRET
- CORS_Origin
- Slack_Username
- Slack_Channel
- Webhook_URL
- Salesforce_OrgId
- Salesforce_WebToLeadURL

"""

import os
import json
import boto3
import requests
import urllib.request
import logging
from collections import OrderedDict
import pprint

def validateCaptcha( captchaResponse ):
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data = {
            'secret': os.environ.get('ReCAPTCHA_SECRET'),
            'response': captchaResponse,
        }
    )
    if not response.ok:
        return False

    data = response.json()
    print('Captcha Response', data)
    return data['success']

def response( statusCode, errors = None ):
    body = {
        'success': True if statusCode == SUCCESS else False,
    }
    if errors is not None:
        body['errors'] = errors
    return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': os.environ.get('CORS_Origin'),
        },
    }

def post_slack(argStr):
    message = argStr
    send_data = {
        "username": os.environ.get('Slack_Username'),
        "text": message,
        "channel": os.environ.get('Slack_Channel')
    }
    send_text = json.dumps(send_data)
    request = urllib.request.Request(
        os.environ.get('Webhook_URL'), 
        data=send_text.encode('utf-8'), 
        method="POST"
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')

def post_salesforce(event):
    params_string = {}
    Items = {
          "oid": os.environ.get('Salesforce_OrgId'),
          "lead_source": event['leadsource'],
          "company": event['customer_name'],
          "email": event['customer_email'],
          "phone": event['customer_phone']
        }
    for key, value in Items.items():
        params_string[key] = value

    response = requests.post(
        os.environ.get('Salesforce_WebToLeadURL'),
        data = params_string
    )
    if not response.ok:
        return False
    return "OK"


def lambda_handler(event, context):
    try:
        form_information = htmlText.format(
            customer_name = event['customer_name'], 
            customer_email = event['customer_email'],
            customer_phone =  event['customer_phone'],
            )
        if validateCaptcha(event['recaptchaResponse']):
            post_slack(form_information)
            post_salesforce(event)
            return "OK"
            print(response.status_code)
            print(response.body)
            print(response.headers)

    except Exception as e:
        print("Error Exception.")
        print(e)
        # print(e.body)
        
htmlText = """
New Lead In Leadsource

Name：{customer_name}
Phone：{customer_phone}
Email：{customer_email}

Check your salesforce Lead
"""
