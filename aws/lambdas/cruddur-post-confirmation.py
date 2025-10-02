import json
import psycopg2
import os

def lambda_handler(event, context):
	user = event['request']['userAttributes']
	print('userAttributes')
	print(user)
	
	user_display_name =user['name']
	user_handle = user['preferred_username']
	user_email = user['email']
	user_cognito_id = user['sub']
	
	try:
		print('entered-try')
		sql = f"""
			INSERT INTO public.users (
				display_name,
				handle,
				email, 
				cognito_user_id
			) 
			VALUES (
				%s,
				%s,
				%s,
				%s
			)
		"""

		parameters = [	
			sql,
			user_uuid,
			message,
			expires_at
		]


		print('----SQL----')
		print(sql)

		conn = psycopg2.connect(os.getenv('PSQL_CRUDDUR_DB_URL'))
		cur = conn.cursor()
		
		cur.execute(sql, *parameters)
		conn.commit()
	
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	
	finally:
		if conn is not None:
			cur.close()
			conn.close()
			print('Database connection closed.')
	
	return event
	