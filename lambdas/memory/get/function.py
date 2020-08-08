from memorial import * 

def handler(event, context):
  conn = psycopg2.connect(host = 'memorial.cogxlpoqzgkf.us-east-2.rds.amazonaws.com', 
                          port = 5432, 
                          dbname = 'memorial', 
                          user = 'postgres', 
                          password = 'science2224')

  cursor = conn.cursor()

  cursor.execute("""
    SELECT * FROM memory
  """)

  columns = [column[0] for column in cursor.description]
  response = cursor.fetchall()
  memory = sql_response_as_dicts(columns, response)

  return http_response(memory)