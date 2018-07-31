import boto3
import os
import json
import datetime

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    now = datetime.datetime.now()
    response = dynamodb.query(
        TableName = 'DYNAMO_TABLE_NAME',
        IndexName = event['pathParameters']['dateToCheck']
    )
    dateScan = dynamodb.scan(
        TableName = 'DYNAMO_TABLE_NAME',
        FilterExpression = str.(now.month)+'/'+(now.day)+'/'+(now.year)
    )
    dataClear = dynamodb.delete_item()
    return "You have successfully signed up for the class on "