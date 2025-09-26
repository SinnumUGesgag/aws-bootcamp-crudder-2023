from datetime import datetime, timedelta, timezone

# PSQL & Psycopg2--->
from lib.db import InteractSQLDB
# <---

class HomeActivities:
  def run(cognito_user_id=None):
    #now = datetime.now(timezone.utc).astimezone()
    end_path = tuple('activities','home')
    sql = InteractSQLDB.template(end_path)

    results = InteractSQLDB.query_json_array(sql)

    return results