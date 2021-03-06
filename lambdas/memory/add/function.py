from memorial import * 

def handler(event, context):
  conn = psycopg2.connect(host = 'memorial.cogxlpoqzgkf.us-east-2.rds.amazonaws.com', 
                          port = 5432, 
                          dbname = 'memorial', 
                          user = 'postgres', 
                          password = 'science2224')

  cursor = conn.cursor()
  payload = json.loads(event['body'])

  cursor.execute("""
    WITH memory_author as (
      insert into author (first_name, last_name, email) values (%s, %s, %s)
      RETURNING id as author_id
    )
    insert into memory (author_id, title, message)
    values( (SELECT author_id FROM memory_author), %s, %s)
    RETURNING *;
  """, (payload['first_name'], payload['last_name'], payload['email'], payload['title'], payload['message']))

  columns = [column[0] for column in cursor.description]
  response = cursor.fetchone()
  memory = sql_response_as_dict(columns, response)
  memory['first_name'] = payload['first_name']
  memory['last_name'] = payload['last_name']
  memory['email'] = payload['email']

  cursor.execute("COMMIT;")

  return http_response(memory)