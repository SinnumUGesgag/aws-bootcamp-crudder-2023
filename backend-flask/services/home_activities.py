from datetime import datetime, timedelta, timezone

# PSQL & Psycopg2--->
from lib.db import db
# <---

class HomeActivities:
  def run(cognito_user_id=None):
    #now = datetime.now(timezone.utc).astimezone()

    sql = db.template('activities','home')

    results = db.query_json_array(sql)

    return results