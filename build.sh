#!/usr/bin/bash

# Run using:
# >source build.sh

# General:
export QUALIFIER="dev"
# AWS CLI:
export AWS_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --query "Account" --output text)
export AWS_DEFAULT_REGION="eu-west-2"
# AWS Stack variables:
export REPO_NAME="api-convert-json-2-csv"
export GIT_COMMIT_ID="manual"
export ARTIFACT_BUCKET="lambda-${QUALIFIER}-artifacts-${AWS_DEFAULT_ACCOUNT}-${AWS_DEFAULT_REGION}"
export LAMBDA_PACKAGE="lambda_a.zip"

# Creating Lambda artifact package
cd lambda_a
zip -qr lambda_a . && aws s3 cp ${LAMBDA_PACKAGE} s3://${ARTIFACT_BUCKET}/${REPO_NAME}/${LAMBDA_PACKAGE} && rm -rf ${LAMBDA_PACKAGE}
cd ..

# Bootstrap process:
cdk bootstrap \
	aws://${AWS_DEFAULT_ACCOUNT}/${AWS_DEFAULT_REGION} \
	--app "python3 cdk.py" \
	--qualifier "${QUALIFIER}" \
	--profile deployment

# Deploy process:
cdk deploy \
	--app "python3 cdk.py" \
	--profile deployment




