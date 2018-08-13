import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DATES_TABLE_NAME'])
    response = table.query(
        KeyConditionExpression=Key('Certification').eq('Cloud Practitioner')
    )

    items = response['Items']

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": items
    }
    return resp