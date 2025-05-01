#!/bin/bash
# Script deletes all versioned object from a bucket.
# use this to get around "Cannot delete S3 bucket because it is not empty
# but it has no (visible) files in it...

aws s3api delete-objects \
    --bucket ${bucket_name} \
    --delete "$(aws s3api list-object-versions \
    --bucket ${bucket_name} \
    --output json \
    --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}')"
