import boto3
import json
from memorial import * 

def handler(event, context):
  bucketLinks = []

  s3 = boto3.client('s3', aws_access_key_id="AKIAZZKD3QOWJHEVVCZU", aws_secret_access_key="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")

  for file in s3.list_objects(Bucket='memorial-images')['Contents']:

    buketLink = 'https://memorial-images.s3.us-east-2.amazonaws.com/' + file['Key']

    bucketLinks.append({ 'id': file['Key'],
                        'imageLink': buketLink })
  print(bucketLinks)
  
  return http_response(bucketLinks