import aws_cdk
from aws_cdk.aws_s3 import CfnBucket
from typing import List
import json

from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    aws_secretsmanager as secretsmanager,
    RemovalPolicy,
    SecretValue,
)

from constructs import Construct
from config.bucket_attributes import BucketAttributes


class PersistenceStack(aws_cdk.Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: aws_cdk.Environment,
        application_ci: str,
        bucket_name: str,
        target_buckets: List[BucketAttributes],
        deploy_replication: bool,
        termination_protection: bool,
        retain_policy: bool,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, env=env, **kwargs)

        removal_policy = RemovalPolicy.DESTROY
        if retain_policy:
            removal_policy = RemovalPolicy.RETAIN

        replication_role = iam.Role(
            self,
            "ReplicationRole",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com"),
        )

        replication_role.assume_role_policy.add_statements(
            iam.PolicyStatement(
                actions=["sts:AssumeRole"],
                principals=[iam.ServicePrincipal("batchoperations.s3.amazonaws.com")],
            )
        )

        target_bucket_objects = []
        if deploy_replication:
            target_bucket_objects = [
                s3.Bucket.from_bucket_attributes(
                    self,
                    id=tb["id"],
                    account=tb["account"],
                    bucket_name=tb["bucket_name"],
                    region=tb["region"],
                )
                for tb in target_buckets
            ]

        self.analytics_bucket = s3.Bucket(
            self,
            "AnalyticsBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=bucket_name,
            enforce_ssl=True,
            versioned=True,
            removal_policy=removal_policy,
        )

        if deploy_replication:
            cfn_bucket: CfnBucket = self.analytics_bucket.node.default_child

            cfn_bucket.replication_configuration = (
                s3.CfnBucket.ReplicationConfigurationProperty(
                    role=replication_role.role_arn,
                    rules=[
                        s3.CfnBucket.ReplicationRuleProperty(
                            destination=s3.CfnBucket.ReplicationDestinationProperty(
                                bucket=bucket.bucket_arn
                            ),
                            status="Enabled",
                        )
                        for bucket in target_bucket_objects
                    ],
                )
            )

            replication_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "s3:GetObjectVersionForReplication",
                        "s3:GetObjectVersionAcl",
                        "s3:GetObjectVersionTagging",
                    ],
                    resources=[
                        self.analytics_bucket.arn_for_objects("*"),
                    ],
                )
            )
            replication_role.add_to_policy(
                iam.PolicyStatement(
                    actions=["s3:ListBucket", "s3:GetReplicationConfiguration"],
                    resources=[
                        self.analytics_bucket.bucket_arn,
                    ],
                ),
            )
            for bucket in target_bucket_objects:
                replication_role.add_to_policy(
                    iam.PolicyStatement(
                        actions=[
                            "s3:ReplicateObject",
                            "s3:ReplicateDelete",
                            "s3:ReplicateTags",
                        ],
                        resources=[
                            bucket.arn_for_objects("*"),
                        ],
                    ),
                )
