from datetime import datetime, timedelta, timezone

from lib.db   import InteractSQLDB
from lib.dydb import InteractDyDb
# from lib.memento import MomentoCounter


class MessageGroups:
  def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }

    data = None
    errors = None
    try:
      pSQLocalUrl = 'PSQL_CRUDDUER_DB_URL'

      sql = InteractSQLDB(pSQLocalUrl).template('/users', '/uuid_from_cognito_user_ids')
      user_returned = InteractSQLDB(pSQLocalUrl).query_user_dict(sql, {'cognito_user_id': cognito_user_id})

      my_user_uuid = user_returned.get('entry_uuid')

      dyDbClient = InteractDyDb.client()
      data = InteractDyDb.list_message_groups(dyDbClient, my_user_uuid)

      if data == []:
        errors = {
          (f"!!!! No Data Returned From DyDb !!!!"),
          (f"---- dyDbClient : {dyDbClient} ||||"),
          (f"---- SQL Passed IN : {sql} ||||"),
          (f"---- MY UUID Returned : {my_user_uuid} ||||")
        }
    except Exception as e:
      errors = {
        e,
        (f"---- SQL Passed IN: {sql} ||||"),
        (f"---- MY UUID Returned: {my_user_uuid} ||||")
      }



    # app.logger.info(f"UUID: {my_user_uuid}")
    # app.logger.info(f"-------- list_message_groups --------")
    # app.logger.info(f"||||---- Data: {data} ||||")

    # #MomentoCounter.reset(f"msgs/{user_handle}"")
    # model[ 'data' ] = data

    model = {
      'errors': errors,
      'data': data
    }

    return model