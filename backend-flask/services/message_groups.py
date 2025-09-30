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

    end_path = tuple('users', 'uuid_from_cognito_user_ids')
    pSQLocalUrl = 'PSQL_CRUDDUER_DB_URL'
    sql = InteractSQLDB(pSQLocalUrl).template(end_path)
    my_user_uuid = InteractSQLDB(pSQLocalUrl).query_value(sql, {'cognito_user_id': cognito_user_id})

    print(f"UUID: {my_user_uuid}")

    dyDbClient = InteractDyDb.client()
    data = InteractDyDb.list_message_groups(dyDbClient, my_user_uuid)
    print(f"-------- list_message_groups --------")
    print(f"||||---- Data: {data} ||||")


    # #MomentoCounter.reset(f"msgs/{user_handle}"")
    # model[ 'data' ] = data
    # return model