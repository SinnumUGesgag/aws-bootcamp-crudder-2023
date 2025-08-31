from datetime import datetime, timedelta, timezone

# PSQL & Psycopg2--->
from lib.db import InteractSQLDB
# <---

class HomeActivities:
  def run(cognito_user_id=None):
    now = datetime.now(timezone.utc).astimezone()

    results = InteractSQLDB.query_json_array("""
    #SELECT * FROM activities
    SELECT 
      activities.uuid,
      users.display.name,
      users.handle,
      activities.replies_count,
      activities.reposts_count,
      activities.likes_count,
      activities.reply_to_activity_uuid,
      activities.expires_at,
      activities.created_at
    FROM public.activities
    LEFT JOIN public.users ON users.uuid = activities.user_uuid
    ORDER BY activities.created_at DESC
    """)

    return result