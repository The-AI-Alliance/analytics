import builtins
from typing import List

import aws_cdk

from persistence_stack.persistence_stack import PersistenceStack
from access_stack.access_stack import AccessStack
from config.bucket_attributes import BucketAttributes


class RegionalStack(aws_cdk.Stack):
    def __init__(
        self,
        scope,
        application_ci: builtins.str,
        env: aws_cdk.Environment,
        id: builtins.str,
        is_primary_region: bool,
        runtime_environment: builtins.str,
        source_bucket: BucketAttributes,
        target_buckets: List[BucketAttributes],
        **kwargs,
    ):

        super().__init__(scope, id, **kwargs)

        persistence_stack = PersistenceStack(
            self,
            "persistence_stack",
            env=env,
            application_ci=application_ci,
            bucket_name=source_bucket["bucket_name"],
            target_buckets=target_buckets,
            deploy_replication=False,
            termination_protection=False,
            retain_policy=True,
        )

        access_stack = AccessStack(
            self,
            "access_stack",
            env=env,
            application_ci=application_ci,
            is_primary_region=is_primary_region,
            bucket=persistence_stack.analytics_bucket,
        )
