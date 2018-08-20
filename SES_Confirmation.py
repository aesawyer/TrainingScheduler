import json
import os
import boto3

def lambda_handler(event, context):
    ses = boto3.client('ses')