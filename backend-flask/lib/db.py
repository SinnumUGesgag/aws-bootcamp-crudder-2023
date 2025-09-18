from psycopg_pool import ConnectionPool
import re
import sys
import os

from flask import current_app as app

class InteractSQLDB:
	def __init__(self):
		self.init_pool()
		# print(f"""------__init__-----""")
		# print("whatever error I am monitoring")

	# intializing the Psycopg Connnectino Pool to our SQL DB
	def init_pool(self):
		connection_url = os.getenv("PSQL_CRUDDUER_DB_URL")
		self.pool = ConnectionPool(connection_url)
		print(f"""------init_pool-----""")
		print(type(self))

	# to INSERT into the SQL DB while utilizing a connection in our Psycopg Connection Pool 
	def query_commit_returning_id(self, sql, params={}):

		# app.logger.info(f"query_commit_returning_id : params : {params} ----------")
		# app.logger.info(f"query_commit_returning_id : sql : {sql} ------------")

		# make sure to check for RETURNING in all uppercases
		pattern = r"\bRETURNING\b"
		is_returning_id = re.search(pattern, sql)

		app.logger.info(f"------  query_commit_returning_id  :  is_returning_id : {is_returning_id} ----------")

		try:
			with self.pool.connection() as conn:
				cur = conn.cursor()
				cur.execute(sql, params)
				if is_returning_id:
					returning_id = cur.fetchone()[0]
				conn.commit()
				if is_returning_id:
						return returning_id
		except Exception as errors:
			app.logger.info(f"----- errors: {errors}")
		# print(f"""------query_commit_returning_id-----""")
		# print("whatever error I am monitoring")

	# to query an array of json objects
	def query_json_array(self, sql, params={}):
		#app.logger.info(f"query_json_array : params : {params} ----------")
		#app.logger.info(f"query_json_array : sql : {sql} ------------")

		# print(f"""------query_json_array-----""")
		# print("whatever error I am monitoring")
		
		wrapped_sql = self.query_wrap_array(sql)	
		with self.pool.connection() as conn:
			with conn.cursor() as cur:
				cur.execute(wrapped_sql, params)
				# this will return a tuple
				# the first field being the data
				json = cur.fetchone()
				return json[0]

	# to query a json object from the DB
	def query_json_object(self, sql, uuid):

		# app.logger.info(f"query_json_object : uuid : {uuid} ----------")
		# app.logger.info(f"query_json_object : sql : {sql} ------------")

		wrapped_sql = self.query_wrap_object(sql)	
		with self.pool.connection() as conn:
			with conn.cursor() as cur:
				cur.execute(wrapped_sql, uuid)
				# this will return a tuple
				# the first field being the data
				json = cur.fetchone()
				if json == None:
					"{}"
				else:
					return json[0]
		# print(f"""------query_json_object-----""")
		# print("whatever error I am monitoring")

	def query_value(self, sql, parameters={}):
		with self.pool.connection() as conn:
			with conn.cursor() as cur:
				cur.execute(sql, parameters)
				json = cur.fetchone()
				return json[0]


	def query_wrap_object(self, sql):
		new_sql = f'''
		(SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
		{sql}
		) object_row);
		'''
		# print(f"""------query_wrap_object-----""")
		# print("whatever error I am monitoring")
		return new_sql

	def query_wrap_array(self, sql):
		new_sql = f'''
		(SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'{{}}'::json) FROM (
		{sql}
		) array_row);
		'''
		# print(f"""------query_wrap_array-----""")
		# print("whatever error I am monitoring")
		return new_sql


	# # to INSERT into the SQL BD & have it return the UUID of the new entry 
	# def query_commit_returning_id(self, sql, *kwargs):

	# 	try:
	# 		conn = self.pool.connection()
	# 		cur = conn.cursor()
	# 		cur.execute(sql, kwargs)
	# 		returning_id = cur.fetchone()[0]
	# 		conn.commit()
	# 		return returning_id
	# 	except Exception as errors:
	# 		app.logger.info(f"----- errors: {errors}")

	def template(self, *args):
		
		# finds the root path listing it as the first entry, then the name of the folders where
		# I've stored the SQL Tempplates; then it lists the args as individual entries

		pathing = list((app.root_path,'db','sql',) + args)
		# adding to the very end of the list ".sql" which is the file type for the SQL files we'll  be referrencing for our SQL Templates
		pathing[-1] = pathing[-1] + ".sql"

		# Joins each individual entry within the Pathing List while then navigating that path to find the file that we're going to read
		template_path = os.path.join(*pathing)
		# opens the file with reading privileges only
		with open(template_path, 'r') as f:
			# reads the file's contents and places them as a string into the template_content variable, to be returned for use as our SQL object that we're going to pass into functions that require an SQL input
			template_content = f.read()
		
		# print(f"""------template-----""")
		# print("whatever error I am monitoring")
		return template_content



#db = InteractSQLDB()

