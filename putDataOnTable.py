#!/usr/bin/env python3

import boto3
from datetime import datetime, timezone

from boto3.dynamodb.conditions import Key, Attr
import json
from botocore.exceptions import ClientError

def get_dynamodb_client():
    dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    return dynamodb

def get_dynamodb_resource():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    return dynamodb

def add_data_to_the_table():
    table_name = get_dynamodb_resource().Table("DirectMessages")

    with table_name.batch_writer() as batch:
        batch.put_item(
            Item={
                'toUsername': 'ProfAvery',
                'messageId': 'c4d0e3e2-d11e-44b5-914d-9e9aa78e46f0',
                'fromUsername': 'KevinAWortman',
                'message':'Hey, Are you free?',
                'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
            }           
        )
        batch.put_item(
            Item={
                'toUsername': 'KevinAWortman',
                'messageId': '1119c6c3-f689-4c10-9b37-a6467c816b0b',
                'fromUsername': 'ProfAvery',
                'message': "Yep, what's up?",               
                'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
            }
        )
        batch.put_item(
            Item={
                'toUsername': 'ProfAvery',
                'messageId': '41675926-d93f-4e95-ac48-0ebb23a69eac',
                'fromUsername': 'KevinAWortman',
                'message':'Do you want to get some boba?',
                'quickReplies': ["Yes", "No", "Call me"],
                'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
            }           
        )
        batch.put_item(
            Item={
                'toUsername': 'KevinAWortman',
                'messageId': '6580cac5-4ca7-45ed-a060-dc41469f4f80',
                'fromUsername': 'ProfAvery',
                'message': "0",
                'in-reply-to': '41675926-d93f-4e95-ac48-0ebb23a69eac',
                'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
            }
        )
        batch.put_item(
            Item={
                'toUsername': 'ProfAvery',
                'messageId': 'f12d35ac-cb90-4870-b3bf-7ffb8d116213',
                'fromUsername': 'KevinAWortman',
                'message': "Where do you want to go?",
                'quickReplies':['OMOMO', 'Share Tea'],
                'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
            }
        )
        batch.put_item(
            Item={
                'toUsername': 'KevinAWortman',
                'messageId': 'fdc7e956-a780-479b-89ed-53677dee9be7',
                'fromUsername': 'ProfAvery',
                'message': "Anywhere is fine",
                'in-reply-to':'f12d35ac-cb90-4870-b3bf-7ffb8d116213',
                'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
            }
        )
if __name__ == '__main__':
    add_data_to_the_table()