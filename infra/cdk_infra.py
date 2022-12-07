# !/usr/bin/env python3
from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
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
                 lambda_layer: str,
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

        # Lambda Layer
        layer = lambda_.LayerVersion(
            scope=self, 
            id='lambda-layer',
            code=lambda_.S3Code(
                bucket=artifact_s3,
                key=f"{repo}/{lambda_layer}"),
            description='json to csv libs',
            layer_version_name=f"{repo}-layer",
            compatible_runtimes=[
                lambda_.Runtime.PYTHON_3_8,
                lambda_.Runtime.PYTHON_3_9
            ],
            compatible_architectures=[
                lambda_.Architecture.X86_64,
                lambda_.Architecture.ARM_64
            ],
            removal_policy=RemovalPolicy.DESTROY
        )

        # Lambda Function
        lambda_a = lambda_.Function(
            scope=self,
            id='lambda-a',
            code=lambda_.S3Code(
                bucket=artifact_s3,
                key=f"{repo}/{lambda_package}"),
            layers=[layer],
            handler="app.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name=f"{repo}-etl",
            role=lambda_role,
            timeout=Duration.seconds(10)
        )

        # CDK outputs
        CfnOutput(scope=self, id='lambda-layer-arn',
                  value=layer.layer_version_arn)
        
        CfnOutput(scope=self, id='lambda-a-arn',
                  value=lambda_a.function_arn)
