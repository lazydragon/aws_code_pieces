import json

def lambda_handler(event, context):
    return {
        'statusCode': '200', 
        #'body': json.dumps(event, sort_keys=True, indent=4), 
        'body': event,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

