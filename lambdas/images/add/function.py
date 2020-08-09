import boto3
import botocore
import botocore.exceptions
import json
import urllib.request
import base64
from memorial import * 

def handler(event, context):
  #print(event)
  rawData = json.loads(event['body'])
  print(rawData)

  s3_bucket = "memorial-images"
  s3_filename = str(rawData['fileName']) + ".png"

  s3_resource = boto3.resource('s3')
  s3 = boto3.client('s3', aws_access_key_id="AKIAZZKD3QOWJHEVVCZU", aws_secret_access_key="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")
  bucket = s3_resource.Bucket(s3_bucket)
  try:
    uri = s3.generate_presigned_url('put_object', Params = {'Bucket': s3_bucket, 'Key': s3_filename}, ExpiresIn = 6000, HttpMethod="PUT")
    print(uri)
    return http_response({"response": uri})
  except Exception as e:
    print(e)
    return http_error_response(("Failed to Execute " + str(e)))
