import os

import aws_cdk
import builtins

from regional_stack import RegionalStack
from constructs import Construct
from config.bucket_attributes import BucketAttributes

account_ids = {
    "dev": os.environ.get("AWS_DEV_ACCOUNT"),
    "qa": os.environ.get("AWS_QA_ACCOUNT"),
    "prd": os.environ.get("AWS_PRD_ACCOUNT"),
}


class RootEnvStack(aws_cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        runtime_environment: str,
        id: builtins.str,
        application_ci: builtins.str,
        **kwargs,
    ):

        super().__init__(scope, id)

        primary_region = "us-east-1"
        secondary_region = "us-east-2"
        bucket_base_name = f"{application_ci}-analytics"

        secondary_bucket = BucketAttributes(
            bucket_name=f"{bucket_base_name}-{secondary_region}",
            region=secondary_region,
            account=account_ids[runtime_environment],
            id=f"{application_ci}-analytics-secondary",
        )

        primary_bucket = BucketAttributes(
            bucket_name=f"{bucket_base_name}-{primary_region}",
            region=primary_region,
            account=account_ids[runtime_environment],
            id=f"{application_ci}-analytics-primary",
        )

        primary_stack = RegionalStack(
            self,
            id=primary_region,
            runtime_environment=runtime_environment,
            env=aws_cdk.Environment(
                account=account_ids[runtime_environment], region=primary_region
            ),
            application_ci=application_ci,
            is_primary_region=True,
            source_bucket=primary_bucket,
            target_buckets=[secondary_bucket],
        )

        # When we are production ready and need fault tolerance...
        secondary_stack = RegionalStack(
            self,
            id=secondary_region,
            runtime_environment=runtime_environment,
            env=aws_cdk.Environment(
                account=account_ids[runtime_environment], region=secondary_region
            ),
            application_ci=application_ci,
            is_primary_region=False,
            source_bucket=secondary_bucket,
            target_buckets=[primary_bucket],
        )
