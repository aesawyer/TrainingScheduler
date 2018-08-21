import json
import os
import boto3

def lambda_handler(event, context):
    data = json.dumps(event)

    ses = boto3.client('ses', region_name=os.getenv('SES_REGION'))
    ses.send_email(
        Source=os.getenv('SES_EMAIL_SOURCE'),
        Destination={'ToAddresses': data['Email']},
        Message={
            'Subject': {'Data': 'AWS Certification Course Confirmation'},
            'Body': {'Data': ['Congratulations ' + data['FirstName'] + ' ' + data['LastName'] + '!/n' 
                'You have successfully signed up for the ' + data['Certification'] + ' course starting on ' + data['StartDate'] + '.']
            }
        }
    )