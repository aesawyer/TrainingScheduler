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
            table.delete_item(
                Key={
                    'StartDate': o['StartDate'],
                    'Email': o['Email']
                }
            )


def date_checker(val):
    # val input "Full Month, Day, Year" (example: "January 1, 1900")
    delimiters = (', ', ' ')
    delim = tuple(delimiters)
    stack = [val, ]

    now = datetime.datetime.now()
    currMon = now.month
    currDay = now.day
    currYear = now.year

    # splits val input into separate Month, Day, and Year
    for d in delim:
        for i, substring in enumerate(stack):
            substack = substring.split(d)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i + j, _substring)
    monthConv = date_converter(stack[0])
    if (monthConv < currMon):
        return (True)
    elif (monthConv == currMon) and (int(stack[1]) <= currDay - 7):
        return (True)
    elif (int(stack[2]) < currYear):
        return (True)


def date_converter(val):
    # Used in-place of strptime due to strptime output
    if val == '01':
        return 1
    elif val == '02':
        return 2
    elif val == '03':
        return 3
    elif val == '04':
        return 4
    elif val == '05':
        return 5
    elif val == '06':
        return 6
    elif val == '07':
        return 7
    elif val == '08':
        return 8
    elif val == '09':
        return 9
    elif val == '10':
        return 10
    elif val == '11':
        return 11
    elif val == '12':
        return 12