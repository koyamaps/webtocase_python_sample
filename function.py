"""
# Enviroment Variables List
- CORS_Origin
- Authorization
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
        if event['auth'] == os.environ.get('Authorization'):
            post_salesforce(event)
            return "OK"
            print(response.status_code)
            print(response.body)
            print(response.headers)

    except Exception as e:
        print("Error Exception.")
        print(e)
        # print(e.body)
        
