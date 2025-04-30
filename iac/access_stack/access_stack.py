import aws_cdk
import json

from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    aws_secretsmanager as secretsmanager,
)

from constructs import Construct


class AccessStack(aws_cdk.Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: aws_cdk.Environment,
        application_ci: str,
        is_primary_region: bool,
        bucket: s3.Bucket,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, env=env, **kwargs)

        if not is_primary_region:
            service_account_username = f"svc-{application_ci}-analytics"

            service_account = iam.User(
                self,
                "IAMUser",
                user_name=service_account_username,
            )

            # TODO: There does not seem to be a secure way to get the access keys
            # for an IAM user and store them in AWS Secrets Manager.
            # You can retreive the access keys as strings, but then they are not
            # "secrets"....
            # Doing this manually via the AWS UI for now.

            # service_account_access_keys = iam.CfnAccessKey(
            #    self, "AccessKeys", user_name=service_account.user_name
            # )

            service_account_access_keys_secret = secretsmanager.Secret(
                self,
                "serviceAccountSecret",
                secret_name=f"{application_ci}/{service_account_username}",
                generate_secret_string=secretsmanager.SecretStringGenerator(
                    secret_string_template=(
                        json.dumps({"aws_access_key_id": "some_junk"})
                    ),
                    generate_string_key="aws_secret_access_key",
                ),
            )

            service_account_policy = iam.Policy(self, "ServiceAccountBuckerReadWrite")

            service_account_policy.add_statements(
                iam.PolicyStatement(
                    actions=[
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:GetObjectTagging",
                        "s3:DeleteObject",
                        "s3:DeleteObjectVersion",
                        "s3:GetObjectVersion",
                        "s3:GetObjectVersionTagging",
                        "s3:GetObjectACL",
                        "s3:PutObjectACL",
                    ],
                    resources=[bucket.arn_for_objects("*")],
                )
            )
            service_account_policy.add_statements(
                iam.PolicyStatement(
                    actions=["s3:ListBucket"],
                    resources=[bucket.bucket_arn],
                )
            )

            service_account.attach_inline_policy(service_account_policy)
