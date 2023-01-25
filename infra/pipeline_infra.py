from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3,
    aws_codepipeline
)
from constructs import Construct


class PipelineStack(Stack):
    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 repo: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # CodePipeline
        pipeline = aws_codepipeline.Pipeline(
            self, id="pipeline",
            pipeline_name=repo
        )

        CfnOutput(scope=self, id="pipeline-arn",
                  value=pipeline.pipeline_arn)
