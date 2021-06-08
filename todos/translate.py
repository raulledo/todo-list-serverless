import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translateAws = boto3.client('translate')
comprehendAws = boto3.client('comprehend')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    # set target language
    target = event['pathParameters']['lang']
    
    # set text
    text = result['Item']['text']
    
    # detect source language
    source_language = detect_language(text)['Languages'][0]['LanguageCode'];
    
    # translate text
    result['Item']['text'] = translate_text(text, source_language, target)['TranslatedText']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response


def detect_language(text):
    return comprehendAws.detect_dominant_language(Text=text)

    
def translate_text(text, source, target):
    return translateAws.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)