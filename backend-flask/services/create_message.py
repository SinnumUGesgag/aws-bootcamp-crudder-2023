import uuid
from lib.db   import InteractSQLDB
from lib.dydb import InteractDyDb

from datetime import datetime, timedelta, timezone


class CreateMessage:
  def run(mode,message,cognito_user_id,message_group_uuid=None,user_receiver_handle=None):

    pSQLocalUrl = 'PSQL_CRUDDUR_DB_URL'

    model = {
      'errors': None,
      'data': None
    }

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
        'handle':  user_sender_handle,
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

      print(f"-------- CreateMessage : Returned by InteractSQLDB : {users} <<<<||||")

      my_user     =   next((item for item in users if item["kind"] == 'sender'), None)
      other_user  =   next((item for item in users if item["kind"] == '????'), None)

      print(f"-------- CreateMesssage :: My User:{my_user} && Other User:{other_user} <<<<||||")

      try:
        errors = {}
        dyDBclient = InteractDyDb.client()
        errors.update({'dyDBclient': dyDBclient})

        if(mode == "Update"):
          model['data'] = InteractDyDb.create_message(
            client=dyDBclient,
            message_group_uuid=message_group_uuid,
            message=message,
            my_user_uuid=my_user['entry_uuid'],
            my_user_display_name=my_user['display_name'],
            my_user_handle=my_user['handle']
          )
        elif (mode == "Create"):
          model['data'] = InteractDyDb.create_message_group(
            client=dyDBclient,
            my_user_uuid=my_user['entry_uuid'],
            my_user_display_name=my_user['display_name'],
            my_user_handle=my_user['handle'],
            other_user_uuid=other_user['entry_uuid'],
            other_user_display_name=other_user['display_name'],
            other_user_handle=other_user['handle']
          )
      except Exception as e:
        errors.update({'InteractDyDb.create_ Exception': e})
       
      errors.update({'System Errors': model['errors']})

      # following error hanlding is used to only test Errors for create_mesage.py       ---->
      # will cause Errors for any other Script/Code that invokes CreateMessage.run()    ---->
      # if (model['errors'] == None):
      #   model['errors'] = {
      #     (f"----- INPUTS : ---- mode : {mode} ||||"),
      #     (f"----- INPUTS : ---- message : {message} ||||"),
      #     (f"----- INPUTS : ---- cognito_user_id : {cognito_user_id} ||||"),
      #     (f"----- INPUTS : ---- message_group_uuid : {message_group_uuid} ||||"),
      #     (f"----- INPUTS : ---- user_receiver_handle : {user_receiver_handle} ||||"),
      #     (f"---- Responses : ---- sql : {sql} ||||"),
      #     (f"---- Responses : ---- users : {users} ||||"),
      #     (f"---- Responses : ---- my_user : {my_user} ||||"),
      #     (f"---- Responses : ---- other_user : {other_user} ||||"),
      #    (f"---- !!!! Responses : !!!! CRITICAL ERRORS : {errors} ||||")
      #   }
      # <----------

    return model