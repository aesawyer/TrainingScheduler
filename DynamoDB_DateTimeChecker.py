import boto3
import json
import decimal
import os
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DATES_TABLE_NAME'])
    response = table.scan()

    items = response['Items']

    # Provides items in ClassDates table to .html for dropdown fill
    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": items
    }
    return resp