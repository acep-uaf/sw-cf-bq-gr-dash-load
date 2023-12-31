#!/bin/bash

# Source the .env file
source eiedeploy.env

# Deploy the function
gcloud functions deploy sw-cw-bq-gr-dash-load \
   --$GEN2 \
   --runtime=$RUNTIME \
   --region=$REGION \
   --service-account=$SERVICE_ACCOUNT \
   --source=$SOURCE \
   --entry-point=$ENTRY_POINT \
   --memory=$MEMORY \
   --timeout=$TIMEOUT  \
   --trigger-topic=$TRIGGER_TOPIC \
   --vpc-connector=$VPC_CONNECTOR \
   --set-env-vars CREATE_DASHBOARD_URL=$CREATE_DASHBOARD_URL,LIST_FOLDERS_URL=$LIST_FOLDERS_URL,SECRET_NAME=$SECRET_NAME,FOLDER_ID=$FOLDER_ID
