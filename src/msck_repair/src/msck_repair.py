# Purpose of code is to execute MSCK REPAIR TABLE
# on all the tables in a given database.
import boto3
import os
from datetime import datetime, timezone
import awswrangler as wr
import pandas as pd

# AWS Athena implements schema-on-read as Hive, need to execute this
# to refresh the data after write in order to query it later.
# MSCK REPAIR TABLE executed as an Athena query.
# TODO: Bucket and region will be passed in from aws cdk when we get there

print(f"Starting job: {datetime.now(timezone.utc)}")
region_name = os.environ["AWS_REGION"]
database_name = os.environ["ATHENA_DATABASE_NAME"]

print(f"region_name: {region_name}")
print(f"database_name: {database_name}")

boto3.setup_default_session(region_name=region_name)
input_df = wr.catalog.tables(database=database_name)

for index, row in input_df.iterrows():
    print(f"Repairing table: {database_name}.{row["Table"]}")
    status = wr.athena.repair_table(database=database_name, table=row["Table"])
    print(f"Status: {status}")
print(f"Ending job: {datetime.now(timezone.utc)}")
