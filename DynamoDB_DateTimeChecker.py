import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DATES_TABLE_NAME')
    response = table.query(
        KeyConditionExpression=Key('Cloud Practitioner')
    )
    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": response
    }
    return resp