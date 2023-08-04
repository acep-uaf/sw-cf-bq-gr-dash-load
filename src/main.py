from google.cloud import storage, secretmanager_v1 as secretmanager
from google.api_core.exceptions import Forbidden, BadRequest, GoogleAPICallError
import logging
import base64
import json
import requests
#import os

def load_gr_dash(event, context):
    print(f'Received event: {event}')  
    logging.info(f'Received event: {event}')
    #grafana_url = "http://10.138.0.26:3000/api/health" # Replace with your Grafana internal IP and port
    create_dashboard_url = "http://10.138.0.26:3000/api/dashboards/db"
    secret_client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/675499914510/secrets/sw-gr-token/versions/1"
    secret_response = secret_client.access_secret_version(name=secret_name)
    secret_value = secret_response.payload.data.decode('UTF-8')
    #headers = {'Authorization': f'Bearer {secret_value}'}
    #headers = {'Authorization': f'Bearer {secret_value}', 'Content-Type': 'application/json'}
    # Headers
    headers = {'Accept': 'application/json','Content-Type': 'application/json','Authorization': f'Bearer {secret_value}'}

    try:
        # Test the connection to Grafana by checking its health
        #response = requests.get(grafana_url, headers=headers)
        #response.raise_for_status() # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        #print(f'Grafana Health Response: {response.json()}')

        # Define the URL to list folders
        list_folders_url = "http://10.138.0.26:3000/api/folders"

        # Send GET request to retrieve the folders
        response = requests.get(list_folders_url, headers=headers)
        response.raise_for_status()  # Check for errors

        # Print the folders
        folders = response.json()
        for folder in folders:
            print(f"ID: {folder['id']}, Title: {folder['title']}")
     
        # JSON Payload
        payload = {
            "dashboard": {
                "title": "New Dashboard",
                "schemaVersion": 16,
                "version": 0
            },
            "folderId": 0,
            "overwrite": False
        }

        # Send POST request
        response = requests.post(create_dashboard_url, json=payload, headers=headers)

        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')  

        # Check for errors
        response.raise_for_status()

        # Print or return the response
        print(response.json())
     

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
