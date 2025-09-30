from uuid import uuid4
from datetime import datetime, timedelta, timezone
from lib.db import InteractSQLDB
from flask import current_app as app

class CreateActivity:
  def run(message, handle, ttl):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if handle == None or len(handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'handle':  handle,
        'message': message
      }   
    else:

      expires_at = (now + ttl_offset).isoformat()
      entry_uuid = CreateActivity.create_activity(handle, message, expires_at)

      app.logger.info(f"UUID returned {entry_uuid}-------")

      object_json = CreateActivity.query_object_activity(entry_uuid)

      model['data'] = {
        'entry_uuid': entry_uuid,
        'display_name': 'Andrew Brown',
        'handle':  handle,
        'message': message,
        'created_at': now.isoformat(),
        'expires_at': expires_at
      }
    return model



  def create_activity(handle, message, expires_at):
    end_path = tuple('activities','create')
    pSQLocalUrl = os.getenv("PSQL_CRUDDUER_DB_URL")
    sql = InteractSQLDB(pSQLocalUrl).template(end_path)
    return InteractSQLDB(pSQLocalUrl).query_commit_returning_id(sql, {
      'handle': handle,
      'message': message,
      'expires_at': expires_at
    })

  def query_object_activity(uuid):
    end_path = tuple('activities','object')
    sql = InteractSQLDB(pSQLocalUrl).template(end_path)
    return InteractSQLDB(pSQLocalUrl).query_json_object(sql,{
      'uuid': uuid
    })

      
