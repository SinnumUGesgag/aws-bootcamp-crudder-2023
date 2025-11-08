import uuid
from lib.db   import InteractSQLDB
from lib.dydb import InteractDyDb

from datetime import datetime, timedelta, timezone


class CreateMessage:
  def run(mode,message,cognito_user_id,message_group_uuid=None,user_receiver_handle=None):

    pSQLocalUrl = 'PSQL_CRUDDUR_DB_URL'

    model = {
      'errors': None,
      'data': None,
      'logging':[]
    }

    inputs_received = {
      'mode':mode,
      'message':message,
      'cognito_user_id':cognito_user_id,
      'message_group_uuid':message_group_uuid,
      'user_receiver_handle':user_receiver_handle
    }

    model['logging'].append(f"inputs_received': {inputs_received}")

    if(mode == "Update"):
      if message_group_uuid == None or len(message_group_uuid) < 1:
        model['errors'] = ['message_group_uuid_blank']
    
      if cognito_user_id == None or len(cognito_user_id) < 1:
        model['errors'] = ['cognito_user_id_blank']

    if(mode == "Create"):
      if user_receiver_handle == None or len(user_receiver_handle) < 1:
        model['errors'] = ['user_receiver_handle_blank']

      if message == None or len(message) < 1:
        model['errors'] = ['message_blank']
      elif len(message) > 1024:
        model['errors'] = ['message_exceed_max_chars']


    if model['errors']:
      # return what we provided
      model['data'] = {
        'display_name': 'Andrew Brown',
        'handle':  user_receiver_handle,
        'message': message
      }
    else:
      sql = InteractSQLDB(pSQLocalUrl).template('/users','/create_message_users')
      if user_receiver_handle == None:
        rev_handle = ''
      else:
        rev_handle = user_receiver_handle
    
      users = InteractSQLDB(pSQLocalUrl).query_json_array(sql,{
        'cognito_user_id': cognito_user_id,
        'user_receiver_handle': rev_handle
      })

      my_user     =   next((item for item in users if item["kind"] == 'sender'), None)
      other_user  =   next((item for item in users if item["kind"] == 'recv'), None)
      
      psql_data = {
        'sql':sql,
        'cognito_user_id':cognito_user_id,
        'user_receiver_handle':user_receiver_handle,
        'my_user':my_user,
        'other_user':other_user
      }

      model['logging'].append(f"psql_data: {psql_data}")
        
      my_user_uuid=my_user['entry_uuid']
      my_user_display_name=my_user['display_name']
      my_user_handle=my_user['handle']

      try:
        other_uuid = other_user['entry_uuid']
      except Exception as e:
        model['logging'].append(f"---- {e}  ||||")
        other_uuid=None


      if  other_uuid == None:
        other_user_uuid=None
        other_user_display_name=None
        other_user_handle=None
      else:
        other_user_uuid=other_user['entry_uuid']
        other_user_display_name=other_user['display_name']
        other_user_handle=other_user['handle']

      try:
        errors = {}
        dyDBclient = InteractDyDb.client()
        errors.update({'dyDBclient': dyDBclient})

        model['logging'].append(f"dyDBclient: {dyDBclient}")

        dyDbResponse = InteractDyDb.create_message_N_update_groups(
          client=dyDBclient,
          message_group_uuid=message_group_uuid,
          message=message,
          my_user_uuid=my_user_uuid,
          my_user_display_name=my_user_display_name,
          my_user_handle=my_user_handle,
          other_user_uuid=other_user_uuid,
          other_user_display_name=other_user_display_name,
          other_user_handle=other_user_handle
        )

        model['logging'].append(f"dyDbResponse: {dyDbResponse}")

        model['data'] = dyDbResponse

      except Exception as e:
        errors.update({'InteractDyDb.create_ Exception': e})
       
      errors.update({'System Errors': model['errors']})

    return model