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

The function uses a VPC connector to securely interface with the Grafana API. To set up this VPC, utilize the provided script: `vpc_connector_deploy.sh`.

```bash
gcloud compute networks vpc-access connectors create vpc-connector-grafana \
  --region=us-west1 \
  --network=default \
  ```

### Cloud Function Deployment

The main deployment script for the function is named `eiedeploy.sh`. This script contains configurations specific to runtime, region, memory allocation, VPC connectivity, and environment variables.

```bash
gcloud functions deploy sw-cw-bq-gr-dash-load \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --service-account=untar-ingest@acep-ext-eielson-2021.iam.gserviceaccount.com \
  --source=src \
  --entry-point=load_gr_dash \
  --memory 16384MB \
  --timeout 540s \
  --trigger-topic sw-cf-gr-ld \
  --vpc-connector projects/acep-ext-eielson-2021/locations/us-west1/connectors/vpc-connector-grafana \
  --set-env-vars PP_TABLE=vtndpp \
  --range=192.168.0.0/28
```

### Dependencies

The Cloud Function relies on the Python packages listed in the `requirements.txt` file. These are crucial for interfacing with Google Cloud services and making external API calls and include the `google-api-core`, `google-cloud-storage`, and `google-cloud-secret-manager` packages.

## Conclusion
 `sw-cw-bq-gr-dash-gen` is a sophisticated Cloud Function tailored to interact with with Grafana, offering a streamlined, automated solution for dashboard management in the cloud.





