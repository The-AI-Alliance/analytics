#!/bin/bash
# Script deletes all versioned object from a bucket.
# use this to get around "Cannot delete S3 bucket because it is not empty
# but it has no (visible) files in it...

aws s3api delete-objects \
    --bucket aaa-analytics-us-east-1 \
    --delete "$(aws s3api list-object-versions \
    --bucket aaa-analytics-us-east-1 \
    --output json \
    --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}')"
