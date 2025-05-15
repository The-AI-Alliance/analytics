#!/bin/bash

docker run \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
-e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
-e AWS_REGION=us-east-2 \
-e AWS_S3_BUCKET=$ANALYTICS_BUCKET \
-e PROJECTS=proscenium,gofannon,sdpk,unitxt \
-e COOL_OFF_S=3 \
-e LOAD_FULL_HX=false \
--network=host \
pypi_analytics