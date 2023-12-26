import boto3
import json
import datetime
import logging
import re
import pytz
import os
from datetime import datetime, time, date
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Set to True to get the lambda to assume the Role attached on the Config Service (useful for cross-account).
ASSUME_ROLE_MODE = False
#table_name = 'AWS-Service-List'
table_name = os.environ['TABLE_NAME']

logger = logging.getLogger(__name__)

def lambda_handler(event, context):

    #global AWS_SERVICE_CLIENT

    #check_defined(event, 'event')
    print(event)
    #config_detail = event['detail']['configurationItem']['configuration']
    #print(config_detail)
    
    #AWS_SERVICE_CLIENT = get_client(services[i], event)
    resourceType = event['detail']['configurationItem']['resourceType']
    tags = event['detail']['configurationItem']['tags']
    region = event['region']

    if region != 'ap-northeast-1':
        print(f"not supported region for testing resourceType: {resourceType}")
        return {
        'statusCode': 404,
        'body': 'not supported region for testing'
    }
    #print(tags)
    
    # Given dictionary
    #data = {'aws:elasticfilesystem:default-backup': 'enabled', 'test': 'true', 'Name': 'cloudcontroltest1'}

    # Check if 'test' key exists with value 'true'
    if 'Retain' in tags and tags['Retain'].lower() == 'true':
        print("'Retain' key with value 'true' exists in the dictionary.")
        status = 'Alive'
    else:
        print("'Retain' key with value 'true' does not exist in the dictionary.")
        status = 'Terminate'
    #print(status)
    resourceId = event['detail']['configurationItem']['resourceId']
    awsRegion = event['detail']['configurationItem']['awsRegion']
    configurationItemStatus = event['detail']['configurationItem']['configurationItemStatus']
    # configurationItemStatus = 'ResourceDeleted'
    if 'resourceName' in event:
        resourceName = event['detail']['configurationItem']['resourceName']
    else:
        resourceName = event['detail']['configurationItem']['resourceId']
    #print(resourceId)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist_timezone).time()
    if current_time_ist.hour > 18:
        time_to_update = 'true'
    else:
        time_to_update = 'false'
    insert_data = {
        'resourceId': resourceId,
        'resourceType': resourceType,
        'resource_status': status,
        'awsRegion': awsRegion,
        'resourceName': resourceName,
        'configurationItemStatus': configurationItemStatus,
        'time_of_crud_past_18': time_to_update
    }
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'resourceId': insert_data['resourceId'], 'resourceType': insert_data['resourceType']})
    #print(response)
    if 'Item' not in response:
        response = table.put_item(Item={'resourceId': insert_data['resourceId'], 'resourceType': insert_data['resourceType'], 'resource_status': insert_data['resource_status'], 'awsRegion': insert_data['awsRegion'], 'resourceName': insert_data['resourceName'], 'configurationItemStatus': insert_data['configurationItemStatus'], 'time_of_crud_past_18': insert_data['time_of_crud_past_18']})
        #'resourceId': insert_data['resourceId'], 'resourceType': insert_data['resourceType'], 'status': insert_data['status'], 'awsRegion': insert_data['awsRegion'], 'resourceName': insert_data['resourceName']
        print('Item inserted successfully.')
    elif response['Item']['resource_status'] != insert_data['resource_status'] or response['Item']['configurationItemStatus'] != insert_data['configurationItemStatus']:
        response = table.update_item(
            Key={'resourceId': insert_data['resourceId'], 'resourceType': insert_data['resourceType']},
            UpdateExpression="set resource_status= :s, configurationItemStatus= :c",
            ExpressionAttributeValues={
                ':s': insert_data['resource_status'],
                ':c': insert_data['configurationItemStatus']
            },
            ReturnValues="ALL_NEW"
            )
        print('Item inserted successfully.')
    else:    
        print('Item with the same id already exists. Not inserting.')

    #response = table.put_item(Item=item)
    return {
        'statusCode': 200,
        'body': 'Completed'
    }
