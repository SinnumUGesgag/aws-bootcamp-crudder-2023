import boto3
import botocore.exceptions
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
        #current_year = datetime.now().year
        table_name = 'cruddur_messages'
        query_parameters = {
            'TableName': table_name,
            #'KeyConditionExpression': 'pk = :pkID AND begins_with(sk,:year)',
            'KeyConditionExpression': 'pk = :pkID',
            'ScanIndexForward': False,
            'Limit': 20,
            'ExpressionAttributeValues': {
            #':year': {'S': f"{current_year}"},
            ':pkID': {'S': f"GRP#{my_user_uuid}"}
            }
        }

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
        
    def create_message_group(client, my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid, other_user_display_name, other_user_handle, last_message_at=None, message=None):
        table_name = 'cruddur_messages'

        message_group_uuid = str(uuid.uuid4())
        message_uuid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).astimezone().isoformat()
        last_message_at = now
        created_at = now

        my_message_group = {
            'pk': {'S': f"GPR#{my_user_uuid}"},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_uuid': {'S': other_user_uuid},
            'user_display_name': {'S': other_user_display_name},
            'user_handle': {'S': other_user_handle}
        }

        other_message_group = {
            'pk': {'S': f"GPR#{other_user_uuid}"},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_uuid': {'S': my_user_uuid},
            'user_display_name': {'S': my_user_display_name},
            'user_handle': {'S': my_user_handle}
        }

        message = {
            'pk': {'S': f"MSG#{message_group_uuid}"},
            'sk': {'S': created_at},
            'message_uuid': {'S': message_uuid},
            'message': {'S': message},
            'user_uuid': {'S': my_user_uuid},
            'user_display_name': {'S': my_user_display_name},
            'user_handle': {'S': my_user_handle}
        }

        items = {
            table_name: [
                {'PutRequest': {'Item': my_message_group}},
                {'PutRequest': {'Item': other_message_group}},
                {'PutRequest': {'Item': message}}
            ]
        }

        try:
            response = client.batch_write_item(RequestItems=items)
            return {
                'message_group_uuid': message_group_uuid,
                # 'uuid': my_user_uuid,
                # 'display_name': my_user_display_name,
                # 'handle': my_user_handle,
                # 'message': message,
                # 'created_at': created_at
            }
        except botocore.exceptions.ClientError as e:
            return(f"-------- DyDb : Create MEssage Groups ERRORs: {e} && CreatedAT: {created_at}")

        # try:
        #     # Transaction - Attempting to Write to the DB
        #     with dynamodb_resource.meta.client.transact_write_items(RequiredItems=items) as transaction:
        #         print(f"|||||||| Transaction Started --------")
        #         aaa
        #         print(f"-------- Transaction Committed ||||||||")
        #         print(f"---- Response: {response} ||||")
        # except ClientError as e:
        #     print(f"---- Client Error: {e} ||||")


    def create_message_N_update_groups(client, message, my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid=None, other_user_display_name=None, other_user_handle=None, message_group_uuid=None):
        
        model = {
            'errors': None,
            'data': None,
            'logging':[]
        }

        inputs_received = {
            'client':client, 
            'message':message, 
            'my_user_uuid':my_user_uuid, 
            'my_user_display_name':my_user_display_name, 
            'my_user_handle':my_user_handle, 
            'other_user_uuid':other_user_uuid, 
            'other_user_display_name':other_user_display_name, 
            'other_user_handle':other_user_handle, 
            'message_group_uuid':message_group_uuid   
        }

        model['logging'].append(f"----  createMessage & Groups -- inputs_received : {inputs_received}  ||||")

        table_name = 'cruddur_messages'
        now = datetime.now(timezone.utc).astimezone().isoformat()
        message_uuid = str(uuid.uuid4())

        last_message_at = now
        created_at = now
        current_year = datetime.now().year
        
        try:
            if message_group_uuid == None:
                # When a New Message Group is being Created then I'll need to create the UUID for it
                message_group_uuid = str(uuid.uuid4())

            if other_user_uuid == None:
                # when Updating Message Groups after creating a Message I will need to query up the Other User's Data
                query_parameters = {
                    'TableName': table_name,
                    'KeyConditionExpression': 'pk = :pkID AND begins_with(sk,:year)',
                    # 'FilterExpression': 'message_group_uuid = :MSG_UUID',
                    'ScanIndexForward': False,
                    'Limit': 20,
                    'ExpressionAttributeValues': {
                        ':year': {'S': f"{current_year}"},
                        #':MSG_UUID': {'S': f"{message_group_uuid}"},
                        ':pkID': {'S': f"GRP#{my_user_uuid}"}
                    }
                }

                response = client.query(**query_parameters)


                items = response['Items']
                # The Items is a Dict within a List, therefore if I am not using a For Loop to work through the list then I need to specify the 0th position within the list to pull the data within it
                item = items[0]

                other_user_uuid = item['user_uuid']['S']
                other_user_display_name = item['user_display_name']['S']
                other_user_handle = item['user_handle']['S']

                #return (f"-----   Testing Failure Point : create_message_N_update_groups triggered : Successful DyDb's results: other_user_uuid:{other_user_uuid} ; other_user_display_name:{other_user_display_name} ; other_user_handle: {other_user_handle} && DyDb's response: {response}  ||||")

        except Exception as e:
            return (f"-----   Testing Failure Point : create_message_N_update_groups triggered : DyDb Searching For Other User : {e} && DyDb's Results: other_user_uuid:{other_user_uuid} ; other_user_display_name:{other_user_display_name} ; other_user_handle: {other_user_handle} && DyDb's response: {response} ||||")


        otherUser_data = {
            'response':response,
            'item': item,
            'other_user_uuid':other_user_uuid,
            'other_user_display_name':other_user_display_name,
            'other_user_handle':other_user_handle
        }

        model['logging'].append(f"----  createMessage & Groups -- otherUser_data : {otherUser_data}  ||||")

        my_message = {
            'pk': {'S': f"MSG#{message_group_uuid}"},
            'sk': {'S': created_at},
            'message_uuid': {'S': message_uuid},
            'message': {'S': message},
            'user_uuid': {'S': my_user_uuid},
            'user_display_name': {'S': my_user_display_name},
            'user_handle': {'S': my_user_handle}
        }

        # Even if I am just Updating an Exsisting Message Group after creating a Message I am still going to need to update the Groups
        # PutRequests in a Batch Write will overwrite the older entry of the same Message Groups
        my_message_group = {
            'pk': {'S': f"GPR#{my_user_uuid}"},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_uuid': {'S': other_user_uuid},
            'user_display_name': {'S': other_user_display_name},
            'user_handle': {'S': other_user_handle}
        }

        

        other_message_group = {
            'pk': {'S': f"GPR#{other_user_uuid}"},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_uuid': {'S': my_user_uuid},
            'user_display_name': {'S': my_user_display_name},
            'user_handle': {'S': my_user_handle}
        }

        model['logging'].append(f"----  createMessage & Groups -- my_message : {my_message}  ||||")
        model['logging'].append(f"----  createMessage & Groups -- my_message_group : {my_message_group}  ||||")
        model['logging'].append(f"----  createMessage & Groups -- other_message_group : {other_message_group}  ||||")
        

        items = {
            table_name: [
                {'PutRequest': {'Item': my_message_group}},
                {'PutRequest': {'Item': other_message_group}},
                {'PutRequest': {'Item': my_message}}
            ]
        }

        try:
            response = client.batch_write_item(RequestItems=items)
            

            model['logging'].append(f"----  createMessage & Groups -- response from batch_write_item : {response}  ||||")
            
            return (f"---- Testing Failure Point : Create Message DyDb PY : batch_write_item items {items} && response {response}  ||||")

            return {
                'message_group_uuid': message_group_uuid,
                # 'uuid': my_user_uuid,
                # 'display_name': my_user_display_name,
                # 'handle': my_user_handle,
                # 'message': message,
                # 'created_at': created_at
            }
        except botocore.exceptions.ClientError as e:
            return(f"-------- DyDb : Create MEssage Groups ERRORs: {e} && CreatedAT: {created_at}")
