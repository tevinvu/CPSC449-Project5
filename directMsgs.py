#!/usr/bin/env python3

import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from botocore.exceptions import ClientError
from uuid import uuid4
import sys
import textwrap
import logging.config
import re
from datetime import datetime, timezone

import bottle
from bottle import get, post, delete, error, abort, request, response, HTTPResponse

app = bottle.default_app()
app.config.load_config('./etc/directMsg.ini')
logging.config.fileConfig(app.config['logging.config'])

# Return errors in JSON
#
# Adapted from # <https://stackoverflow.com/a/39818780>
#
def json_error_handler(res):
    if res.content_type == 'application/json':
        return res.body
    res.content_type = 'application/json'
    if res.body == 'Unknown Error.':
        res.body = bottle.HTTP_CODES[res.status_code]
    return bottle.json_dumps({'error': res.body})

app.default_error_handler = json_error_handler

# Disable warnings produced by Bottle 0.12.19.
#
#  1. Deprecation warnings for bottle_sqlite
#  2. Resource warnings when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings
    for warning in [DeprecationWarning, ResourceWarning]:
        warnings.simplefilter('ignore', warning)

def get_dynamodb_client():
    dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    return dynamodb

def get_dynamodb_resource():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    return dynamodb

#check a key of a dictionary
def checkKey(dict, key):
    if key in dict.keys():
        return True
    else:
        return False

#Routes
@post('/users/<username>/directMessages/')
def sendDirectMessage(username):
    user = request.json
    if not user:
        abort(400)
    posted_fields = user.keys()
    required_fields = {'from', 'message'}

    if not required_fields <= posted_fields:
        abort(400, f"Missing fields: {required_fields - posted_fields}")

    quickReplies_Check = checkKey(user, "quickReplies")
    
    try:
        if quickReplies_Check:
            itemResponse = get_dynamodb_resource().Table("DirectMessages").put_item(
                Item={
                    'toUsername': username,
                    'messageId': str(uuid4()),
                    'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                    'fromUsername': user['from'],
                    'message': user['message'],                                            
                    'quickReplies': user['quickReplies']
                }
            )
        else:
            itemResponse = get_dynamodb_resource().Table("DirectMessages").put_item(
                Item={
                    'toUsername': username,
                    'messageId': str(uuid4()),
                    'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                    'fromUsername': user['from'],
                    'message': user['message']
                }
            )
        logging.debug('A direct message added successfully')
        logging.debug(str(itemResponse))
    except Exception as error:
        abort(409, str(error))

    response.status = 201
    return f"{user['from']} are successful to send a message to {username}"


@post('/users/<username>/directMessages/<messageId>/') 
def replyToDirectMessage(username, messageId):
    logging.debug(username)
    logging.debug(messageId)
    replyMsg = request.json
    if not replyMsg:
        abort(400)
    posted_fields = replyMsg.keys()
    required_fields = {'message'}
    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')
    
    logging.debug(type(username))
    logging.debug(type(messageId))
    try:
        getResponse = get_dynamodb_resource().Table("DirectMessages").get_item(
            Key={
                'toUsername':username,
                'messageId':messageId
            }           
        )
        logging.debug(getResponse)
    except ClientError as error:
        abort(400, error.getResponse['Error']['Message'])
    else:
        if checkKey(getResponse, 'Item'):
            item = getResponse['Item']
            try:
                if replyMsg['message'].isnumeric():
                    replyDM = get_dynamodb_resource().Table("DirectMessages").put_item(
                        Item = {
                            'toUsername': item['fromUsername'],
                            'messageId': str(uuid4()),
                            'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                            'fromUsername': username,
                            'message': replyMsg['message'],
                            'in-reply-to': messageId
                        }
                    )
                else:
                    replyDM = get_dynamodb_resource().Table("DirectMessages").put_item(
                        Item = {
                            'toUsername': item['fromUsername'],
                            'messageId': str(uuid4()),
                            'timestamps': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                            'fromUsername': username,
                            'message': replyMsg['message']
                        }
                    )
            except Exception as error:
                abort(409, str(error))
        else:
            abort(400, "Either username or messageId is not correct")    

    response.status = 201
    return f"{username} has replied to {item['fromUsername']}"
    
    
@get('/users/<username>/directMessages/')
def listDirectMessagesFor(username):
    try:
        uName_response = get_dynamodb_resource().Table("DirectMessages").query(
                KeyConditionExpression=Key('toUsername').eq(username)
            )
        logging.debug(uName_response)
        
    except Exception as error:
        abort(409, str(error))
    if not uName_response['Items']:
            abort(400, "Username is not corrected or Username doesn't have any direct message")
    else:
        response.status = 200
        return {'user': uName_response['Items']}    


@get('/users/<username>/directMessages/<messageId>/')
def listRepliesTo(username, messageId):
    try:
        reply_resp = get_dynamodb_resource().Table("DirectMessages").query(
            KeyConditionExpression=Key('toUsername').eq(username)
        )
        reply_list = []   #list of in-reply-to to the messageId
        logging.debug(reply_resp['Items'])
        temp_replies = reply_resp['Items']
        
        
        #check if any 'in-reply-to' match with the messageId
        for item in temp_replies:
            isInReplyTo = checkKey(item, 'in-reply-to')
            if isInReplyTo:
                if item['in-reply-to'] == messageId:                   
                    logging.debug(f" Check in-reply-to :{item['in-reply-to']}")
                    reply_list.append(item)
                    logging.debug(f"Message Reply to: {item}")

        #if the message reply is a numeric--> turn it into the string message
        for item in reply_list:
            if item['message'].isnumeric():
                try:
                    resp = get_dynamodb_resource().Table("DirectMessages").get_item(
                        Key={
                            'toUsername':item['fromUsername'],
                            'messageId':messageId
                            }
                        )
                    logging.debug(resp)
                    temp_current_resp= resp['Item']
                    quickReplies_list = temp_current_resp['quickReplies']
                    item['message'] = quickReplies_list[int(item['message'])]
                    logging.debug(f"yo: {item['message']}")
                except Exception as error:
                    abort(409, str(error))
    except Exception as error:
        abort(409, str(error))
    if not reply_list:
        abort(400, "Username or messageId is not correct")
    else:
        response.status = 200
        return {username: reply_list}
    
    


    

    