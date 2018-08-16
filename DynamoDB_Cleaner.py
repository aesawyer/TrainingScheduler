import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import datetime


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['ROSTER_TABLE_NAME'])
    classTable = dynamodb.Table(os.environ['CLASS_TABLE_NAME'])
    rosterScan = table.scan()
    # KeyConditionExpression=Key('StartDate').eq(loadedBody['StartDate']),
    # FilterExpression=Attr('Certification').contains(loadedBody['Certification'])

    rosterItems = rosterScan['Items']
    rosterJSON = json.dumps(rosterItems)
    loadedRoster = json.loads(rosterJSON)

    for o in loadedRoster:
        # print(o['StartDate'])
        print(date_checker(o['StartDate']))


'''
        if date_checker(o['StartDate']):
            classTable.delete_item(
                Key={
                    'Certification': loadedBody['Certification'],
                    'StartDate': loadedBody['StartDate']
                }
            )
'''


def date_checker(val):
    delimiters = (', ', ' ')
    delim = tuple(delimiters)
    stack = [val, ]

    now = datetime.datetime.now()
    currMon = now.month
    currDay = now.day
    currYear = now.year
    # today = (now.strftime("%B") + ' ' + str(now.day) + ', ' + str(now.year))

    for d in delim:
        for i, substring in enumerate(stack):
            substack = substring.split(d)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i + j, _substring)
    return stack