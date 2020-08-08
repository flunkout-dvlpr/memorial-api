import sys
import os
import configparser
import boto3
import json
from datetime import date, datetime
import psycopg2

# Required for the PostgreSQL library.
sys.path.insert(0, '/opt')

env = os.environ['ENV']
app_config_path = os.environ['APP_CONFIG_PATH']

def json_serial(obj):
  """JSON serializer for objects not serializable by default json code"""

  if isinstance(obj, (datetime, date)):
    return obj.isoformat()
  raise TypeError ("Type %s not serializable" % type(obj))


def sql_response_as_dicts(columns, sql_response):
  response_as_dicts = []
  for row in sql_response:
    response_as_dicts.append(sql_response_as_dict(columns, row))

  return response_as_dicts

def sql_response_as_dict(columns, sql_response):
  return dict(zip(columns, sql_response))

def dict_as_json(dict_object):
  return json.dumps(dict_object, default=json_serial)

def response_in_json(columns, response):
  response_as_dicts = sql_response_as_dicts(columns, response)
  return json.dumps(response_as_dicts, default=json_serial)

def http_typed_response(responseType, message, payload, statusCode):
  if responseType in ['success', 'error', 'warning', 'info']:
    return {
      'statusCode': statusCode,
      'headers': {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      'body': dict_as_json({
        'type': responseType,
        'message': message,
        'payload': payload
      })
    }
  else:
    raise Exception("Incorrect response type.")

def http_response(payload = {}, message = 'OK'):
  return http_typed_response('success', message, payload, 200)

def http_error_response(message, payload = None):
  return http_typed_response('error', message, payload, 200)

def connect_postgresql(config):

  host = config.get('database', 'host')
  port = config.get('database', 'port')
  name = config.get('database', 'name')
  user = config.get('database', 'user')
  password = config.get('database', 'password')

  conn = psycopg2.connect(host = host, port = port, dbname = name, user = user, password = password)

  cursor = conn.cursor()
  return cursor


class MyApp:
  def __init__(self, config):
    self.config = config

  def get_config(self):
    return self.config


# Initialize app at global scope for reuse across invocations. Kinda like a Singleton
app = None

def init_lambda():
  global app

  full_config_path = '/' + env + '/' + app_config_path

  print("init_lambda called")
  print(env)
  print(app_config_path)
  print(full_config_path)

  # Initialize app if it doesn't yet exist
  # if app is None:
  config = load_config(full_config_path, 'database')
  app = MyApp(config)

  return app

def load_config(ssm_parameter_path, section):
  configuration = configparser.ConfigParser()
  try:
    client = boto3.client('ssm')
    param_details = client.get_parameters_by_path(
      Path="/".join([ssm_parameter_path, section]),
      Recursive=False,
      WithDecryption=True
    )

    # Loop through the returned parameters and populate the ConfigParser
    config_dict = {section: {}}
    if 'Parameters' in param_details:
      for param in param_details.get('Parameters'):
        config_name_segments = param.get('Name').split("/")
        config_section = config_name_segments[-2]
        config_name = config_name_segments[-1]
        config_value = param.get('Value')
        config_dict[config_section][config_name] = config_value
    configuration.read_dict(config_dict)
  except:
    print("Encountered an error loading config from SSM.")
  finally:
    return configuration
