from datetime import datetime, timedelta, timezone

# PSQL & Psycopg2--->
from lib.db import InteractSQLDB
# <---

class HomeActivities:
  def run(cognito_user_id=None):
    pSQLocalUrl = 'PSQL_CRUDDUER_DB_URL'
    sql = InteractSQLDB(pSQLocalUrl).template('/activities','/home')

    results = InteractSQLDB(pSQLocalUrl).query_json_array(sql)

    return results