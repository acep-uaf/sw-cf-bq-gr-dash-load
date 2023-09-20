from google.cloud import storage, secretmanager_v1 as secretmanager
from google.api_core.exceptions import Forbidden, BadRequest, GoogleAPICallError
import logging
import base64
import json
import requests
import os

def load_gr_dash(event, context):
    print(f'Received event: {event}')  
    logging.info(f'Received event: {event}')
    create_dashboard_url = os.environ.get('CREATE_DASHBOARD_URL')
    secret_client = secretmanager.SecretManagerServiceClient()
    secret_name = os.environ.get('SECRET_NAME')
    secret_response = secret_client.access_secret_version(name=secret_name)
    secret_value = secret_response.payload.data.decode('UTF-8')
    headers = {'Accept': 'application/json','Content-Type': 'application/json','Authorization': f'Bearer {secret_value}'}

    try:
        list_folders_url = os.environ.get('LIST_FOLDERS_URL')
        # Send GET request to retrieve the folders
        response = requests.get(list_folders_url, headers=headers)
        response.raise_for_status()  # Check for errors

        # Print the folders
        folders = response.json()
        for folder in folders:
            print(f"ID: {folder['id']}, Title: {folder['title']}")
     

        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_dict = json.loads(pubsub_message)

        project_id = message_dict.get('project_id')
        archive_bucket = message_dict.get('archive_bucket')
        dash_id = message_dict.get('dash_id')

        print(f'project_id : {project_id}')
        print(f'archive_bucket : {archive_bucket}')
        print(f'dash_id : {dash_id}')

        # Read JSON from bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(archive_bucket)
        blob = bucket.blob(dash_id)
        json_content = json.loads(blob.download_as_text())

        print(f'json_content : {json_content}')

        # JSON Payload
        payload = {
            "dashboard": json_content,
            "folderId": 3,
            "overwrite": True
        }

        # Send POST request
        response = requests.post(create_dashboard_url, json=payload, headers=headers)

        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')  

        # Check for errors
        response.raise_for_status()

        # Print or return the response
        print(response.json())
    
    except Forbidden as e:
        print(f'Forbidden error occurred: {str(e)}. Please check the Cloud Function has necessary permissions.')
        raise e
    except BadRequest as e:
        print(f'Bad request error occurred: {str(e)}. Please check the query and the table.')
        raise e
    except GoogleAPICallError as e:
        print(f'Google API Call error occurred: {str(e)}. Please check the API request.')
        raise e
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        raise e
