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
   --set-env-vars PP_TABLE=$PP_TABLE
