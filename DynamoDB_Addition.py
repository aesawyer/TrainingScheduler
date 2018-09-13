import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import smtplib


def lambda_handler(event, context):
    data = json.dumps(event)
    loadedData = json.loads(data)
    body = loadedData['body']  # string
    loadedBody = json.loads(body)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['ROSTER_TABLE_NAME'])
    classTable = dynamodb.Table(os.environ['CLASS_TABLE_NAME'])

    table.put_item(
        Item={
            'StartDate': loadedBody['StartDate'],
            'Email': loadedBody['Email'],
            'FirstName': loadedBody['FirstName'],
            'LastName': loadedBody['LastName'],
            'Certification': loadedBody['Certification']
        }
    )

    ses = boto3.client('ses', region_name=os.getenv('SES_REGION'))
    email = ses.send_email(
        Source=os.environ['SES_EMAIL_SOURCE'],
        Destination={
            'ToAddresses': [
                os.environ['SES_EMAIL_SOURCE']
            ],
        },
        Message={
            'Subject': {
                'Data': 'New Attendee for ' + loadedBody['Certification'] + ' Certification Training!',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': loadedBody['FirstName'] + ' ' + loadedBody['LastName'] + ' has signed up for the ' +
                            loadedBody['Certification'] + ' course on ' + loadedBody['StartDate'],
                    'Charset': 'UTF-8'
                }
            }
        }
    )

    query = table.query(
        KeyConditionExpression=Key('StartDate').eq(loadedBody['StartDate']),
        FilterExpression=Attr('Certification').contains(loadedBody['Certification'])
    )

    # Removes class from ClassDates table if at or above threshhold (15)
    if len(query['Items']) >= 15:
        classTable.delete_item(
            Key={
                'Certification': loadedBody['Certification'],
                'StartDate': loadedBody['StartDate']
            }
        )

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": body
    }
    return resp