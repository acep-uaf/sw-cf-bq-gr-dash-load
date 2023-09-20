#!/bin/bash

# Source the .env file
source vpc_connector.env

# Create the VPC Access Connector
gcloud compute networks vpc-access connectors create $CONNECTOR_NAME \
  --region=$REGION \
  --network=$NETWORK \
  --range=$RANGE