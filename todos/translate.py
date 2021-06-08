# change: test cd/ci
import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    # set target language
    target = event['pathParameters']['id']
    
    # set text
    text = result['Item']['text']
    
    # detect source language
    source_language = detect_language(text);
    
    # translate text
    result['Item']['text'] = translate_text(text, source_language, target)['TranslateText']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response


def detect_language(text):
    return comprehend.detect_dominant_language(text='string')

    
def translate_text(text, source, target):
    return translate.traslate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)