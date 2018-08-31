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
    ses = boto3.client('ses', region_name=os.getenv('SES_REGION'))
    ses.send_email(
        Source=os.getenv('SES_EMAIL_SOURCE'),
        Destination={'ToAddresses': tuple(loadedBody['Email'])},
        Message={
            'Subject': {
                'Data': 'AWS Certification Course Confirmation',
                'Charset': 'UTF-8',
            },
            'Body': {
                'Text': {
                    'Data': 'Congratulations ' + loadedBody['FirstName'] + ' ' + loadedBody['LastName'] + '! ' + 'You have successfully signed up for the ' + loadedBody['Certification'] + ' course starting on ' + loadedBody['StartDate'] + '.',
                    'Charset': 'UTF-8',
                }
            }
        },
        ReturnPath='adam.sawyer@wgu.edu',
        ReturnPathArn='arn:aws:ses:us-east-1:918283516283:identity/adam.sawyer@wgu.edu'
    )
    print(type(loadedData['Email']))
    '''
    #Sends Confirmation Email
    s = smtplib.SMTP()
    s.connect('email-smtp.us-east-1.amazonaws.com', 587)
    s.starttls()
    s.login(os.getenv('SMTP_ACCESS'), os.getenv('SMTP_SECRETACCESS'))
    msg = 'Subject: AWS Certification Course Confirmation\n\nTestEmail'
    # From:'+os.getenv('SES_EMAIL_SOURCE')+'\nTo:'+loadedBody['Email']+'\n
    s.sendmail(os.getenv('SES_EMAIL_SOURCE'), loadedBody['Email'], msg)
    s.close()

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