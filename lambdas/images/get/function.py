import boto3
import json
from memorial import * 

def handler(event, context):

  s3 = boto3.resource('s3')

  imagesBucket = s3.Bucket('memorial-images')

  bucketLinks = []
  for file in imagesBucket.objects.all():
      buketLink = 'https://memorial-images.s3.us-east-2.amazonaws.com/' + file.key

      bucketLinks.append({ 'id': file.key,
                           'imageLink': buketLink })
  return http_response(bucketLinks)