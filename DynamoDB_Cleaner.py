import boto3
import os
import json

def lambda_handler(event, context):
    table = boto3.resource('dynamodb')

    return "You have successfully signed up for the class on "