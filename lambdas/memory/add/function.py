from memorial import * 

def handler(event, context):
  print("someText")
  return http_response({'result': 'success'})