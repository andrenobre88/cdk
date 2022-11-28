#!/usr/bin/env python3

import os
import aws_cdk as cdk

from aws_cdk import (
    aws_lambda as lambda_,
    aws_iam as iam_,
    aws_s3 as s3,
    Tags, Duration, Stack
)

from constructs import Construct


class Infra(Stack):
    def __init__(self, scope: Construct, construct_id: str, repo: str,
                 artifact_bucket: str, lambda_key_a: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM Role
        lambda_role = iam_.Role(scope=self,
                                id=f"{repo}-lambda-role",
                                assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'),
                                role_name=f"{repo}-lambda-role",
                                managed_policies=[
                                    iam_.ManagedPolicy.from_aws_managed_policy_name(
                                        'service-role/AWSLambdaBasicExecutionRole')
                                ])
        # Lambda code artifact bucket
        artifact_s3 = s3.Bucket.from_bucket_attributes(
            self, 'lambda-artifact-bucket',
            bucket_name=artifact_bucket
        )

        # Lambda Function
        lambda_a = lambda_.Function(
            scope=self,
            id=f"{repo}-lambda-a",
            code=lambda_.S3Code(
                bucket=artifact_s3,
                key=lambda_key_a),
            handler="app.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            architecture=None,
            current_version_options=None,
            description=None,
            environment=None,
            function_name=f"{repo}-etl",
            initial_policy=None,
            insights_version=None,
            layers=None,
            log_retention=None,
            log_retention_retry_options=None,
            log_retention_role=None,
            memory_size=None,
            reserved_concurrent_executions=None,
            role=lambda_role,
            timeout=Duration.seconds(10)
        )
        # Adding Tags to Lambda
        Tags.of(lambda_a).add("Repository", repo)

        # CDK outputs
        cdk.CfnOutput(scope=self, id='cdk-lambda-a-output',
                      value=lambda_a.function_name)


app = cdk.App()

Infra(app,
      'andrenobre-cdk',
      env=cdk.Environment(
          account=os.getenv('CDK_DEFAULT_ACCOUNT'),
          region=os.getenv('CDK_DEFAULT_REGION'),
      ),
      repo=os.getenv('REPO_NAME'),
      artifact_bucket=os.getenv('ARTIFACT_BUCKET'),
      lambda_key_a=os.getenv('LAMBDA_KEY_A')
      )

app.synth()
