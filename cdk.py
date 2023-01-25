# !/usr/bin/env python3
import os
import aws_cdk

from aws_cdk import DefaultStackSynthesizer

from infra.pipeline_infra import PipelineStack
from infra.app_infra import AppStack

app = aws_cdk.App()

env_stack = {
    'account_id': os.getenv('AWS_DEFAULT_ACCOUNT'),
    'region': os.getenv('AWS_DEFAULT_REGION'),
    'environment': os.getenv('QUALIFIER'),
    'repo': os.getenv('REPO_NAME'),
    'artifact_bucket': os.getenv('ARTIFACT_BUCKET'),
    'lambda_layer': os.getenv('LAMBDA_LAYER'),
    'lambda_package': os.getenv('LAMBDA_PACKAGE')
}

env_cdk = aws_cdk.Environment(
    account=env_stack['account_id'],
    region=env_stack['region']
)

PipelineStack(app,
              f"{env_stack['repo']}-pipeline-{env_stack['environment']}",
              env=env_cdk,
              synthesizer=DefaultStackSynthesizer(
                qualifier=env_stack['environment']
              ),
              repo=env_stack['repo']
              )

AppStack(app,
         f"{env_stack['repo']}-app-{env_stack['environment']}",
         env=env_cdk,
         synthesizer=DefaultStackSynthesizer(
            qualifier=env_stack['environment']
         ),
         repo=env_stack['repo'],
         artifact_bucket=env_stack['artifact_bucket'],
         lambda_layer=env_stack['lambda_layer'],
         lambda_package=env_stack['lambda_package']
         )

app.synth()
