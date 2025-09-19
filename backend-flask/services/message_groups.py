from datetime import datetime, timedelta, timezone

# from lib.db   import InteractSQLDB
# from lib.dydb import InteractDyDb
# from lib.memento import MomentoCounter


class MessageGroups:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }

    # Adding ---------------- >
    # sql = InteractSQLDB.template('users', 'uuid_from_handle')
    # my_user_uuid = InteractSQLDB.query_value(sql, {'handle': user_handle})

    # print(f"UUID: {my_user_uuid}")

    # InteractDyDb.client()
    # data = InteractDyDb.list_message_groups({unknown_reqInput_ddb}, my_user_uuid)
    # print(f"-------- list_message_groups --------")
    # print(f"||||---- Data: {data} ||||")


    # #MomentoCounter.reset(f"msgs/{user_handle}"")
    # model[ 'data' ] = data
    # return model


    # < ------------------------

    now = datetime.now(timezone.utc).astimezone()
    results = [
      {
        'uuid': '24b95582-9e7b-4e0a-9ad1-639773ab7552',
        'display_name': 'Andrew Brown',
        'handle':  'andrewbrown',
        'created_at': now.isoformat()
      },
      {
        'uuid': '417c360e-c4e6-4fce-873b-d2d71469b4ac',
        'display_name': 'Worf',
        'handle':  'worf',
        'created_at': now.isoformat()
    }]
    model['data'] = results
    return model