import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DATES_TABLE_NAME')
    response = table.query(
        KeyconditionExpression=Key('Cloud Practitioner')
    )