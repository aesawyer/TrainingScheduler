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
    '''
    s = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
    s.ehlo()
    s.starttls()
    s.login('AKIAJUIHL4EXT7C7ASXQ', 'AqKGzXTF1zjP8UM26NY4NjTqfTDrhZsq0pSqQNQ2HWWN')
    msg= 'Subject: AWS Certification Course Confirmation\n\nTestEmail'
    s.sendmail('adam.sawyer@wgu.edu', loadedBody['Email'], msg)
    s.close()
    '''
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