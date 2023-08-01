gcloud functions deploy sw-cw-bq-gr-dash-load \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --source=src \
  --entry-point=load_gr_dash \
  --memory 16384MB \
  --timeout 540s  \
  --trigger-topic sw-cf-gr-ld \
  --set-env-vars PP_TABLE=vtndpp