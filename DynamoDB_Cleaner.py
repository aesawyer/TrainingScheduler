import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import datetime


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    rosterTable = dynamodb.Table(os.environ['ROSTER_TABLE_NAME'])
    classTable = dynamodb.Table(os.environ['CLASS_TABLE_NAME'])
    rosterScan = rosterTable.scan()

    rosterItems = rosterScan['Items']  # Pulls items from scan
    rosterJSON = json.dumps(rosterItems)  # Converts to string
    loadedRoster = json.loads(rosterJSON)  # Convert to dict for category sorting

    for o in loadedRoster:
        if date_checker(o['StartDate']):
            classTable.delete_item(
                Key={
                    'Certification': o['Certification'],
                    'StartDate': o['StartDate']
                }
            )
            rosterTable.delete_item(
                Key={
                    'StartDate': o['StartDate'],
                    'Email': o['Email']
                }
            )


def date_checker(val):
    # val input "Numerical Month/Numberical Day/Full Year" (example: "01/21/2018")
    delim = '/'
    stack = [val]

    now = datetime.datetime.now()
    currMon = now.month
    currDay = now.day
    currYear = now.year

    # splits val input into separate Month, Day, and Year
    for i, substring in enumerate(stack):
        substack = substring.split(delim)
        stack.pop(i)
        for j, _substring in enumerate(substack):
            stack.insert(i + j, _substring)

    if (int(stack[0]) < currMon):
        return (True)
    elif (int(stack[0]) == currMon) and (int(stack[1]) <= currDay):
        return (True)
    elif (int(stack[2]) < currYear):
        return (True)