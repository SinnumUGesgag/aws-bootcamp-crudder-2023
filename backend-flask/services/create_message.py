import uuid
from lib.db   import InteractSQLDB
from lib.dydb import InteractDyDb
# from lib.memento import MomentoCounter
from datetime import datetime, timedelta, timezone


class CreateMessage:
  def run(mode, message, cognito_user_id, message_group_uuid=None, user_receiver_handle=None):
    model = {
      'errors': None,
      'data': None
    }

    if(mode == "update"):
      if message_group_uuid == None or len(message_group_uuid) < 1:
        model['errors'] = ['message_group_uuid_blank']
    
      if cognito_user_id == None or len(cognito_user_id) < 1:
        model['errors'] = ['cognito_user_id_blank']

    if(mode == "create"):

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
      rev_handle = user_receiver_handle
    
    pSQLocalUrl = 'PSQL_CRUDDUR_DB_URL'
    users = InteractSQLDB(pSQLocalUrl).query_json_array(sql,{
      'cognito_user_id': cognito_user_id,
      'user_receiver_handle': rev_handle
    })

    print(f"-------- CreateMessage : Returned by InteractSQLDB : {users} <<<<||||")

    my_user     =   next((item for item in users if item["kind"] == 'sender'), None)
    other_user  =   next((item for item in users if item["kind"] == '????'), None)

    print(f"-------- CreateMesssage :: My User:{my_user} && Other User:{other_user} <<<<||||")

    dyDBclient = InteractDyDb.client()

    if(mode == "update"):
      data = InteractDyDb.create_message(
        client=dyDBclient,
        message_group_uuid=message_group_uuid,
        message=message,
        my_user_uuid=user['entry_uuid']
        my_user_display_name=user['display_name']
        my_user_handle=user['handle']
      )







      now = datetime.now(timezone.utc).astimezone()
      model['data'] = {
        'uuid': uuid.uuid4(),
        'display_name': 'Andrew Brown',
        'handle':  user_sender_handle,
        'message': message,
        'created_at': now.isoformat()
      }
    return model