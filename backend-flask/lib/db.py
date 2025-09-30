from psycopg_pool import ConnectionPool
from flask import current_app as app
import re
import sys
import os

# Add variable pSQLocalUrl for reasons N1 & N2
#	N1 	:	At times the InteractSQLDB is invoked in scripts that are ran at setup  and do not 
# 	have the same resources available as the Container; additionally...
# 	N2	:	The Backend-Flask Container sees the PSQL Local Instance as "db:5342" where as the Gitpod container 
# 	sees the PSQL Local Instance as LocalHost:5432 which means where this Class is invoked affects what URL is needed

class InteractSQLDB:
	def __init__(self, pSQLocalUrl):

		valid_d = 'PSQL_CRUDDUER_DB_URL'
		valid_l = 'PSQL_CRUDDUER_LH_URL'
		
		# small security measure to make sure the PSYCOPG pool isn't somehow manipulated incorrectly
		if (pSQLocalUrl == valid_d):
			pSQLocalUrl = os.getenv("PSQL_CRUDDUER_DB_URL")
		elif (pSQLocalUrl == valid_l):
			pSQLocalUrl = 'postgresql://postgres:password@localhost:5432/cruddur'
		else:
			pSQLocalUrl = None
			print(f"-------- Incorrect or No PSQL URL --------")

		self.init_pool(pSQLocalUrl)
		# print(f"""------__init__-----""")
		# print("whatever error I am monitoring")

	# intializing the Psycopg Connnectino Pool to our SQL DB
	def init_pool(self, pSQLocalUrl):
		self.pool = ConnectionPool(pSQLocalUrl)
		print(f"""------init_pool-----""")
		print(f"---- Self Type: {type(self)} ||||")
		print(f"---- Connection URL: {pSQLocalUrl} ||||")


	def query_commit(self, sql, params={}):
		try:
			typeSelf = type(self)
			print(f"--- self type : {typeSelf}")
			with self.pool.connection() as conn:
				cur = conn.cursor()
				cur.execute(sql, params)
				conn.commit()
		except Exception as errors:
			print(f"----- query_commit errors: {errors}")



	# to INSERT into the SQL DB while utilizing a connection in our Psycopg Connection Pool 
	# Also returns the User UUID
	def query_commit_returning_id(self, sql, params={}):

		# print(f"query_commit_returning_id : params : {params} ----------")
		# print(f"query_commit_returning_id : sql : {sql} ------------")

		# make sure to check for RETURNING in all uppercases
		pattern = r"\bRETURNING\b"
		is_returning_id = re.search(pattern, sql)

		print(f"------  query_commit_returning_id  :  is_returning_id : {is_returning_id} ----------")

		try:
			with self.pool.connection() as conn:
				cur = conn.cursor()
				cur.execute(sql, params)
				conn.commit()
		except Exception as errors:
			print(f"----- query_commit_returning_id errors: {errors}")
			

	# to query an array of json objects
	def query_json_array(self, sql, params={}):
		#print(f"query_json_array : params : {params} ----------")
		#print(f"query_json_array : sql : {sql} ------------")

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

		# print(f"query_json_object : uuid : {uuid} ----------")
		# print(f"query_json_object : sql : {sql} ------------")

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


	def template(self, *end_path):
		
		# finds the root path listing it as the first entry, then the name of the folders where
		# I've stored the SQL Tempplates; then it lists the args as individual entries
		root_i = str(app.root_path)
		path_i = list('')

		path_i.extend(root_i)
		path_i.extend(['/db','/sql'])
		path_i.extend(end_path)
		path_i.extend(".sql")
		pathing = ''.join(path_i)

		# Joins each individual entry within the Pathing List while then navigating that path to find the file that we're going to read
		template_path = os.path.join(pathing)
		# opens the file with reading privileges only
		with open(template_path, 'r') as f:
			# reads the file's contents and places them as a string into the template_content variable, to be returned for use as our SQL object that we're going to pass into functions that require an SQL input
			template_content = f.read()
		
		# print(f"""------template-----""")
		# print("whatever error I am monitoring")
		return template_content



#db = InteractSQLDB()

