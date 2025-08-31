from psycopg_pool import ConnectionPool
import os

class InteractSQLDB:
	def __init__(self):
		self.init_psycopgConnectionPool()

	# intializing the Psycopg Connnectino Pool to our SQL DB
	def init_psycopgConnectionPool(self):
		connection_url = os.getenv("PSQL_CRUDDUER_DB_URL")
		self.pool = ConnectionPool(connection_url)

	def query_wrap_object(self, template):
		sql = f'''
		(SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
		{template}
		) object_row);
		'''
		return sql

	def query_wrap_array(self, template):
		sql = f'''
		(SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'{{}}'::json) FROM (
		{template}
		) array_row);
		'''
		return sql

	def print_sql_errors(self, errors):
		# get details about the exception
		errors_type, errors_obj, traceback = sys.exc_info()

		# get the line number when exception occured
		line_num = traceback.tb_lineno

		# print the connect() error
		print ("\npsycopg ERROR:", errors, "on line number:", line_num)
		print ("psycopg traceback:", traceback, "--- type:", err_type)

		# psycopg2 extensions.Diagnostics object attribute
		print ("\npsycopg.Diagnostics::", errors.diag)
		
		# print the pgcode and pg error exceptions
		print ("pgerror:", errors.pgerror)
		print ("pgcode:", errors.pgcode)

	# to INSET into the SQL DB while utilizing a connection in our Psycopg Connection Pool 
	def query_commit(self):
		try:
			conn = self.pool.connection()
			cur = conn.cursor()
			cur.execute(sql)
			conn.commit()
		except Exception as errors:
			self.print_sql_err(errors)
			#conn.rollback()

	# to query an array of json objects
	def query_json_array(self, sql):
		wrapped_sql = self.query_wrap_array(sql)	
		with self.pool.connection() as conn:
			with conn.cursor() as cur:
				cur.execute(wrapped_sql)
				# this will return a tuple
				# the first field being the data
				json = cur.fetchone()
		return json[0]


	# to query a json object from the DB
	def query_json_object(self, sql):
		wrapped_sql = self.query_wrap_object(sql)	
		with self.pool.connection() as conn:
			with conn.cursor() as cur:
				cur.execute(wrapped_sql)
				# this will return a tuple
				# the first field being the data
				json = cur.fetchone()
		return json[0]