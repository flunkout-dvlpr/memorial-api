import boto3
import json
from memorial import * 

def handler(event, context):
  print(json.dumps(event))
  rawData = json.loads(event['body'])

  s3_bucket = "memorial-images"
  s3_filename = str(rawData['fileName']) + ".jepg"

  s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRETE_KEY)
  try:
    uri = s3.generate_presigned_url('put_object', Params = {'Bucket': s3_bucket, 'Key': s3_filename}, ExpiresIn = 6000, HttpMethod="PUT")
    print(uri)
    return http_response({"response": uri})
  except Exception as e:
    print(e)
    return http_error_response(("Failed to Execute " + str(e)))
