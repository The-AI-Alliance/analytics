#!/bin/bash
poetry export -f requirements.txt --without-hashes >requirements.txt
docker build --network=host --progress=plain --no-cache -t msck_repair .
docker tag msck_repair:latest $ECR_TARGET/fargate-jobs-01/msck_repair:latest
rm requirements.txt