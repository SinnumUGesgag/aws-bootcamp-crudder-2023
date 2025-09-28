from datetime import datetime, timedelta, timezone

# PSQL & Psycopg2--->
from lib.db import InteractSQLDB
# <---

class HomeActivities:
  def run(cognito_user_id=None):
    sql = InteractSQLDB().template('/activities','/home')

    results = InteractSQLDB().query_json_array(sql)

    return results