import aws_cdk

from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
)

from constructs import Construct


class SqlStack(aws_cdk.Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: aws_cdk.Environment,
        application_ci: str,
        output_bucket_retain_policy: bool,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, env=env, **kwargs)

        removal_policy = RemovalPolicy.DESTROY
        if output_bucket_retain_policy:
            removal_policy = RemovalPolicy.RETAIN

        self.analytics_bucket = s3.Bucket(
            self,
            "SqlOutputBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=f"{application_ci}-sql-output-{env.region}",
            enforce_ssl=True,
            versioned=False,
            removal_policy=removal_policy,
        )


# For Athena itself...
# "There are no official hand-written (L2) constructs for this service yet. Here are some suggestions on how to proceed:"
# https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_athena/README.html

# Manual steps...
# 1. Create Workgroup
#    a. Name
#    b. Analytics Engine - Athena SQL / automatics upgrades
#    c. Authentication - AWS IAM Identity Center (W3 SSO)
#    d. Service Role - Create new
#    e. Query output S3 bucket
# 2. Create a database 'aialliance' under data catalog AwsDataCatalog
# 3. Add tables to database 'aialliance' using Hive SQL. See ./sql folder.
