#!/usr/bin/env python3

import os
import aws_cdk as cdk

from aws_cdk import (
    aws_lambda as lambda_,
    Stack, Duration
)

from constructs import Construct


class Infra(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda A
        with open("lambda_a/lambda_handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambda_a = lambda_.Function(
            self, "Singleton",
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=Duration.seconds(10),
            runtime=lambda_.Runtime.PYTHON_3_8,
        )


app = cdk.App()

Infra(app,
      "api-v1",
      env=cdk.Environment(
          account=os.getenv('CDK_DEFAULT_ACCOUNT'),
          region=os.getenv('CDK_DEFAULT_REGION')
          ),
      )

app.synth()
