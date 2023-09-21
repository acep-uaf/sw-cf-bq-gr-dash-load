# SW-CW-BQ-GR-DASH-LOAD Cloud Function

The `sw-cw-bq-gr-dash-load` is a Cloud Function primarily designed to interface with Grafana API, automating the process of dashboard creation and management by reading JSON configurations from Google Cloud Storage. With integrated error handling and VPC connectivity, it operates seamlessly in a controlled and secure environment.

## Functionality Overview

The `load_gr_dash` function leverages the Google Cloud Storage and Secret Manager services, combined with external calls to Grafana's API, to facilitate dashboard-related operations. On a high level:

1. Decodes the event payload and logs the received event.
2. Extracts Grafana's authentication token from Google Secret Manager.
3. Lists Grafana folders.
4. Fetches the dashboard JSON configuration from the specified Cloud Storage bucket.
5. Calls the Grafana API to create the dashboard from the fetched JSON configuration.

### Exception Handling

For robustness, the function has been equipped with intricate exception handling. It captures specific Google Cloud-related exceptions such as `Forbidden`, `BadRequest`, and `GoogleAPICallError`. Furthermore, any unforeseen errors are also caught and appropriately logged.

## Deployment

The deployment of the function and associated resources like the VPC connector involves the use of the `gcloud` command-line tool. The deployment scripts have been delineated into separate shell scripts for clarity and modularity:

### VPC Connector Deployment

To establish secure interfacing with the Grafana API, a VPC connector is utilized. Deploy it using the `vpc_connector_deploy.sh` script:

```bash
#!/bin/bash

# Source the .env file
source vpc_connector.env

# Create the VPC Access Connector
gcloud compute networks vpc-access connectors create $CONNECTOR_NAME \
  --region=$REGION \
  --network=$NETWORK \
  --range=$RANGE
  ```

### vpc_connector.env File Configuration
Before deploying the Cloud Function, ensure that the `vpc_connector.env` file contains the necessary environment variables, as the deployment script sources this file. This file should define values for:

```
CONNECTOR_NAME=<value>
REGION=<value>
NETWORK=<value>
RANGE=<value>
```

### Environment Variable Descriptions
 
Below are descriptions for each environment variable used in the deployment script:

- **CONNECTOR_NAME**=`<value>`:
  - Description: Specifies the name of the VPC Access Connector. This name is used when creating the VPC connector and should be unique within the region. For example, `vpc-connector-grafana` to uniquely identify the Grafana VPC connector.
  
- **REGION**=`<value>`:
  - Description: The Google Cloud region where the VPC Access Connector will be created. This should match the region where your Cloud Function and resources reside. Common values include `us-west1`, `europe-west1`, etc.
  
- **NETWORK**=`<value>`:
  - Description: Specifies the VPC network that the connector should be connected to. Typically set to `default` unless you have a custom VPC network setup in your GCP project.
  
- **RANGE**=`<value>`:
  - Description: The IP CIDR range to use for the VPC Access Connector. This should be a reserved range that does not overlap with any other IP ranges in use in the VPC. For example, `192.168.0.0/28` to specify a subnet in the private IP space.


### Cloud Function Deployment

The main deployment script for the function is named `eiedeploy.sh`. This script contains configurations specific to runtime, region, memory allocation, VPC connectivity, and environment variables.

```bash
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
```
### eiedeploy.env File Configuration
Before deploying the Cloud Function, ensure that the eiedeploy.env file contains the necessary environment variables, as the deployment script sources this file. This file should define values for:

```
GEN2=<value>
RUNTIME=<value>
REGION=<value>
SERVICE_ACCOUNT=<value>
SOURCE=<value>
ENTRY_POINT=<value>
MEMORY=<value>
TIMEOUT=<value>
TRIGGER_TOPIC=<value>
VPC_CONNECTOR=<value>
SECRET_NAME=<value>
CREATE_DASHBOARD_URL=<value>
LIST_FOLDERS_URL=<value>
FOLDER_ID=<value>
```
Replace `<value>` with the appropriate values for your deployment.

### Environment Variable Descriptions
 
Below are descriptions for each environment variable used in the deployment script:

```
GEN2=<value>:
Description: Specifies the generation of the Cloud Function to deploy. For example: gen2 when you intend to deploy a second generation Google Cloud Function.

RUNTIME=<value>:
Description: Specifies the runtime environment in which the Cloud Function executes. For example: python311 for Python 3.11.

REGION=<value>:
Description: The Google Cloud region where the Cloud Function will be deployed and run. Example values are us-west1, europe-west1, etc.

SERVICE_ACCOUNT=<value>:
Description: The service account email associated with the Cloud Function. This determines the permissions the Cloud Function will have.

SOURCE=<value>:
Description: Path to the source code of the Cloud Function. Typically, this points to a directory containing all the necessary files for the function.

ENTRY_POINT=<value>:
Description: Specifies the name of the function or method within the source code to be executed when the Cloud Function is triggered.

MEMORY=<value>:
Description: The amount of memory to allocate for the Cloud Function. This is denoted in megabytes, e.g., 16384MB.

TIMEOUT=<value>:
Description: The maximum duration the Cloud Function is allowed to run before it is terminated. Expressed in seconds, e.g., 540s.

TRIGGER_TOPIC=<value>:
Description: The Google Cloud Pub/Sub topic that triggers the Cloud Function when a message is published to it.

VPC_CONNECTOR=<value>:
Description: Specifies the VPC connector that the Cloud Function uses to connect to services inside the VPC.

SECRET_NAME=<value>:
Description: The name of the secret in Google Secret Manager which holds sensitive data, like API keys or authentication tokens.

CREATE_DASHBOARD_URL=<value>:
Description: The URL endpoint for the Grafana API to create or update a dashboard.

LIST_FOLDERS_URL=<value>:
Description: The URL endpoint for the Grafana API to list all folders.

FOLDER_ID=<value>:
Description: The ID of the Grafana folder where the dashboard should be saved.
```

### Dependencies

The Cloud Function relies on the Python packages listed in the `requirements.txt` file. These are crucial for interfacing with Google Cloud services and making external API calls and include the `google-api-core`, `google-cloud-storage`, and `google-cloud-secret-manager` packages.

## Conclusion
 `sw-cw-bq-gr-dash-gen` is a sophisticated Cloud Function tailored to interact with with Grafana, offering a streamlined, automated solution for dashboard management in the cloud.





