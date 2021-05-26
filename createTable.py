#!/usr/bin/env python3

import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from botocore.exceptions import ClientError

def get_dynamodb_client():
    dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    return dynamodb

def get_dynamodb_resource():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    return dynamodb

def create_table():
    table_name = "DirectMessages"

    attribute_definitions = [
        {
            'AttributeName': 'toUsername',
            'AttributeType': 'S',            
        },
        {
            'AttributeName': 'messageId',
            'AttributeType': 'S'
        }
    ]

    key_schema = [
        {
            'AttributeName': 'toUsername',
            'KeyType':'HASH'
        },
        {
            'AttributeName':'messageId',
            'KeyType':'RANGE'
        }
    ]

    intial_iops = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }

    table_response = get_dynamodb_client().create_table(
        AttributeDefinitions = attribute_definitions,
        TableName = table_name,
        KeySchema = key_schema,
        ProvisionedThroughput=intial_iops       
    )

    print("Create DynamoDB table" + str(table_response))

def get_item_on_table():
    try:
        response = get_dynamodb_resource().Table("DirectMessages").query(
            KeyConditionExpression=Key('toUsername').eq('ProfAvery')
        )
    except ClientError as error:
        print(error.response['Error']['Message'])
    else:
        # print(response)
        items = response['Items']

        print("Got the item successfully")
        print(items)

if __name__ == '__main__':
    create_table()
    # get_item_on_table()       #comment this line out to get the specific item
