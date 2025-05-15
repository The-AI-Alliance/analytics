#!/bin/bash
poetry export -f requirements.txt --without-hashes >requirements.txt
docker build --network=host --progress=plain --no-cache -t pypi_analytics .
docker tag pypi_analytics:latest $ECR_TARGET/fargate-jobs-01/pypi_analytics:latest
rm requirements.txt