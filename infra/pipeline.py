from aws_cdk import (
    Stack,
    CfnOutput,
    aws_codepipeline,
    SecretValue,
    pipelines as pipelines
)
from constructs import Construct


class PipelineStack(Stack):
    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 repo: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Source
        source = pipelines.CodePipelineSource.git_hub(
            "andrenobre88/cdk", "master",
            authentication=SecretValue.secrets_manager("shared/github/token")
        )

        # Pipeline
        pipeline = pipelines.CodePipeline(
            self,
            repo,
            self_mutation=False,
            synth=pipelines.ShellStep(
                "Synth",
                input=source,
                commands=[
                    "npm ci",
                    "npm run build",
                    "npx cdk synth"
                ],
                primary_output_directory="cdk.out"
            )
        )

