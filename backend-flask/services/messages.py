from datetime import datetime, timedelta, timezone
from lib.db   import InteractSQLDB
from lib.dydb import InteractDyDb
# from lib.memento import MomentoCounter

class Messages:
  def run(message_group_uuid,cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }

    data = None
    errors = None
    try:
      # need to use this to verify user is the correct
      # user before showing them the messages of the group  ---->
      pSQLocalUrl = 'PSQL_CRUDDUR_DB_URL'
      sql = InteractSQLDB(pSQLocalUrl).template('/users', '/uuid_from_cognito_user_ids')
      user_returned = InteractSQLDB(pSQLocalUrl).query_user_dict(sql, {'cognito_user_id': cognito_user_id})
      my_user_uuid = user_returned.get('entry_uuid') 
      # < ----

      dyDbClient = InteractDyDb.client()
      data = InteractDyDb.list_messages(dyDbClient, message_group_uuid)

      if data == []:
        errors = {
          (f"!!!! No Data Returned From DyDb !!!!"),
          (f"---- MY USER UUID Returned : {my_user_uuid} ||||"),
          (f"---- dyDbClient : {dyDbClient} ||||"),
          (f"---- MY Message Group UUID Passed into DyDb Client: {message_group_uuid} ||||"),
          (f"||||^^^^ ERRORS ABOVE ^^^^||||")
        }
    except Exception as e:
      errors = {
        e,
          (f"!!!! Verify Containers, Endpoints, & DyDbClient !!!!"),
          (f"---- MY USER UUID Returned : {my_user_uuid} ||||"),
          (f"---- dyDbClient : {dyDbClient} ||||"),
          (f"---- MY MS Group UUID Passed into DyDb Client: {message_group_uuid} ||||"),
          (f"||||^^^^ ERRORS ABOVE ^^^^||||")
      }

    # #MomentoCounter.reset(f"msgs/{user_handle}"")
    # model[ 'data' ] = data

    model = {
      'errors': errors,
      'data': data
    }

    return model