import json
import psycopg2

def lambda_handler(event, context):
	user = event['request']['userAttributes']
	
	user_display_name =user['name']
	user_handle = user['prefered_username']
	user_email = user['email']
	user_cognito_id = user['sub']
	
	try:
		sql = f"""
			"INSERT INTO public.users (
				display_name,
				handle,
				email, 
				cognito_user_id
			) 
			VALUES (
				{user_display_name},
				{user_handle},
				{user_email},
				{user_cognito_id}
			)"
		"""
		
		conn = psycopg2.connect(os.getnev('CONNECTION_URL'))
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
	
	except (Exceptioon, psycopg2.DatabaseError) as error:
		print(error)
	
	finally:
		if conn is not None:
			cur.close()
			conn.close()
			print('Database connection closed.')
	
	return event