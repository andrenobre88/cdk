# !/usr/bin/env python3

import os
import aws_cdk as cdk

from aws_cdk import DefaultStackSynthesizer
from infra.cdk_infra import AppStack

app = cdk.App()

AppStack(app,
         'api-convert-json-2-csv',
         synthesizer=DefaultStackSynthesizer(
             qualifier=os.getenv('QUALIFIER')
         ),
         env=cdk.Environment(
             account=os.getenv('AWS_DEFAULT_ACCOUNT'),
             region=os.getenv('AWS_DEFAULT_REGION'),
         ),
         repo=os.getenv('REPO_NAME'),
         artifact_bucket=os.getenv('ARTIFACT_BUCKET'),
         lambda_package=os.getenv('LAMBDA_PACKAGE')
         )

app.synth()
