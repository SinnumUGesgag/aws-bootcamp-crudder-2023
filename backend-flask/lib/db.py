from psycopg_pool import ConnectionPool
import os

def query_wrap_object(template):
	sql = f'''
	(SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
	{template}
	) object_row);
	'''

def query_wrap_array(template):
	sql = f'''
	(SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'{{}}'::json) FROM (
	{template}
	) array_row);
	'''

connection_url = os.getenv("PSQL_CRUDDUER_DB_URL")
pool = ConnectionPool(connection_url)

