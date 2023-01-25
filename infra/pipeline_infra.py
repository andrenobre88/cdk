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

        # Artifact Bucket
        s3_bucket = aws_s3.Bucket(
            self, id="artifact-bucket",
            bucket_name=f''
                        f'deployment-artifacts-'
                        f'{Stack.of(self).account}-'
                        f'{Stack.of(self).region}',
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            encryption=aws_s3.BucketEncryption.KMS,
            bucket_key_enabled=True
        )

        CfnOutput(scope=self, id="bucket-arn",
                  value=s3_bucket.bucket_arn)

        # CodePipeline
        # pipeline = aws_codepipeline.Pipeline(
        #     self, id="pipeline",
        #     pipeline_name=repo
        # )
        #
        # CfnOutput(scope=self, id="pipeline-arn",
        #           value=pipeline.pipeline_arn)
