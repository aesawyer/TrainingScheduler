import boto3
import os
import json

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.query(
        TableName = 'DYNAMO_TABLE_NAME',
        IndexName = event['pathParameters']['dateToCheck']


    )
    try:
        enterData = dynamodb.put_item(
            TableName = 'DYNAMO_TABLE_NAME',
            Item = {
                'S': event['pathParameters']['dateToCheck']
            },
            ConditionExpression = 'attribute_not_exists',
        )
    except ConditionalCheckFailedException:
        pass
    return "You have successfully signed up for the class on "