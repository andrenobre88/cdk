# !/usr/bin/env python3
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
    aws_iam as iam_,
    aws_s3 as s3
)

from constructs import Construct


class AppStack(Stack):
    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 repo: str,
                 artifact_bucket: str,
                 lambda_package: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM Role
        lambda_role = iam_.Role(scope=self,
                                id='lambda-role',
                                assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'),
                                role_name=f"{repo}-lambda-role",
                                managed_policies=[
                                    iam_.ManagedPolicy.from_aws_managed_policy_name(
                                        'service-role/AWSLambdaBasicExecutionRole')
                                ])
        # Lambda code artifact bucket
        artifact_s3 = s3.Bucket.from_bucket_attributes(
            self, 'artifact-bucket',
            bucket_name=artifact_bucket
        )

        # Lambda Function
        lambda_a = lambda_.Function(
            scope=self,
            id='lambda-a',
            code=lambda_.S3Code(
                bucket=artifact_s3,
                key=f"{repo}/{lambda_package}"),
            handler="app.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name=f"{repo}-etl",
            role=lambda_role,
            timeout=Duration.seconds(10)
        )

        # CDK outputs
        CfnOutput(scope=self, id='lambda-a-name',
                  value=lambda_a.function_name)
