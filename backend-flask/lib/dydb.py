import boto3
import sys
from datetime import datetime, timedelta, timezone
import uuid
import os

class InteractDyDb:
    def client():
        endpoint_url = os.getenv('AWS_DYDB_ENDPOINT_URL')
        #endpoint_url = "http://dynamodb-local:8000"
        attributes = {}
        if endpoint_url:
            attributes = {'endpoint_url': endpoint_url}

        dyanmoDB = boto3.client('dynamodb', **attributes)
        return dyanmoDB
    
    def list_message_groups(client, my_user_uuid):
        current_year = datetime.now().year
        table_name = 'cruddur_messages'
        query_parameters = {
            'TableName': table_name,
            'KeyConditionExpression': 'pk = :pkID AND begins_with(sk,:year)',
            #'KeyConditionExpression': 'pk = :pkID',
            'ScanIndexForward': False,
            'Limit': 20,
            'ExpressionAttributeValues': {
            ':year': {'S': f"{current_year}"},
            ':pkID': {'S': f"GRP#{my_user_uuid}"}
            }
        }
        # print(f"-------- Query Inputs --------")
        # print(f"|||| ---- Query Parameters: {query_parameters} ||||")
        # print(f"|||| ---- With Client: {client} ||||")

        response = client.query(**query_parameters)
        items = response['Items']
        results = []

        for item in items:
            last_sent_at     = item['sk']['S']
            results.append({
                'uuid': item['message_group_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': last_sent_at
            })
        return results
    
    def list_messages(client, message_group_uuid):
        current_year = datetime.now().year
        table_name = 'cruddur_messages'
        query_parameters = {
            'TableName': table_name,
            'KeyConditionExpression': 'pk = :pkID AND begins_with(sk,:year)',
            #'KeyConditionExpression': 'pk = :pkID',
            'ScanIndexForward': False,
            'Limit': 20,
            'ExpressionAttributeValues': {
                ':year': {'S': f"{current_year}"},
                ':pkID': {'S': f"MSG#{message_group_uuid}"}
            }
        }

        response = client.query(**query_parameters)
        items = response['Items']
        items.reverse() # returns the items in a descending order instead of ascending order
        results = []

        for item in items:
            created_at     = item['sk']['S']
            results.append({
                'uuid': item['message_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': created_at
            })
        return results
        
def create_message_group(client, message_group_uuid, my_user_uuid, other_user_uuid, other_user_display_name, other_user_handle, last_message_at=None, message=None):
    table_name = 'cruddur_messages'

    message_group_uuid = str(uuid.uuid4())
    message_uuid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).astimezone().isoformat()
    last_message_at = now
    create_at = now

    message_group = {
        'pk': {'S': f"GPR#{my_user_uuid}"},
        'sk': {'S': last_message_at},
        'message_group_uuid': {'S': message_group_uuid},
        'message': {'S': message},
        'user_uuid': {'S': other_user_uuid},
        'user_display_name': {'S': other_user_display_name},
        'user_handle': {'S': other_user_handle}
    }

    message = {
        'pk': {'S': f"MSG#{message_group_uuid}"},
        'sk': {'S': created_at},
        'message_uuid': {'S': message_group_uuid},
        'message': {'S': message},
        'user_uuid': {'S': user_uuid},
        'user_display_name': {'S': user_display_name},
        'user_handle': {'S': user_handle}
    }

    items = {
        table_name: [
            {'Put': {'Item': message_group}},
            {'Put': {'Item': message}}
        ]
    }

    return {
        'message_group_uuid': message_group_uuid,
        'uuid': my_user_uuid,
        'display_name': my_user_display_name,
        'handle': my_user_handle,
        'message': message,
        'created_at': created_at
    }

    try:
        # Transaction - Attempting to Write to the DB
        with dynamodb_resource.meta.client.transact_write_items(RequiredItems=items) as transaction:
            print(f"|||||||| Transaction Started --------")
            aaa
            print(f"-------- Transaction Committed ||||||||")
            print(f"---- Response: {response} ||||")
    except ClientError as e:
        print(f"---- Client Error: {e} ||||")


def R(client, message_group_uuid, created_at, message, my_user_uuid, my_user_display_name, my_user_handle):
    now = datetime.now(timezone.utc).astimezone().isoformat()
    created_at = now
    message_uuid = str(uuid.uuid4())

    record = {
        'pk': {'S': f"MSG#{message_group_uuid}"},
        'sk': {'S': created_at},
        'message_uuid': {'S': message_uuid},
        'message': {'S': message},
        'user_uuid': {'S': my_user_uuid},
        'user_display_name': {'S': my_user_display_name},
        'user_handle': {'S': my_user_handle}
    }

    # insert into table
    table_name = 'cruddur_messages'
    response = client.put_item(
        TableName=table_name,
        Item=record
    )


    print(f"---- client Response: {response} ||||")

    return{
        'message_group_uuid': message_group_uuid,
        'uuid': my_user_uuid,
        'display_name': my_user_display_name,
        'handle': my_user_handle,
        'message': message,
        'created_at': created_at
    }