from lib.db import InteractSQLDB

class UsersShort:
    def run(handle):
        pSQLocalUrl = 'PSQL_CRUDDUR_DB_URL'
        sql = InteractSQLDB(pSQLocalUrl).template('/users','/short')
        results = InteractSQLDB(pSQLocalUrl).query_json_object(sql,{
            'handle': handle
        })
        # !!!! I am noticing he's got querying json object and yet he's passing the handle and not a uuid into it...even thought it was originally made to require a UUID so I'll have to fix that
        return results