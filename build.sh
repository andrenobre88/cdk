#!/usr/bin/bash
# Run using:
# >source build.sh

# General:
export QUALIFIER="dev" \
	AWS_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --query "Account" --output text) \
	AWS_DEFAULT_REGION="eu-west-2"

# CDK infra
export REPO_NAME="api-convert-json-2-csv" \
	GIT_COMMIT_ID="manual" \
	ARTIFACT_BUCKET="deployment-${QUALIFIER}-artifacts-${AWS_DEFAULT_ACCOUNT}-${AWS_DEFAULT_REGION}" \
	LAMBDA_LAYER="${GIT_COMMIT_ID}/lambda_layer.zip" \
	LAMBDA_PACKAGE="${GIT_COMMIT_ID}/lambda_a.zip"

# Package and Upload
package_upload () {
	[ ! -d "tmp" ] && mkdir tmp
	[[ ! -z "$3" ]] && pip3 install -r $3 -t ./tmp || cp -R $1/ tmp/
	cd tmp && ls -lha 
	zip -qr $2 . && aws s3 cp $2 s3://"${ARTIFACT_BUCKET}"/"${REPO_NAME}"/"${GIT_COMMIT_ID}"/$2
	cd .. && rm -rf tmp
}

# Creating Lambda artifact package
package_upload lambda_layer "${LAMBDA_LAYER}" requirements-layer.txt

# Creating Lambda artifact package
package_upload lambda_a "${LAMBDA_PACKAGE}"

# Bootstrap process:
cdk bootstrap \
	aws://"${AWS_DEFAULT_ACCOUNT}"/"${AWS_DEFAULT_REGION}" \
	--app "python3 cdk.py" \
	--qualifier "${QUALIFIER}" \
	--profile deployment

# Deploy process:
cdk deploy \
	--app "python3 cdk.py" \
	--all \
	--profile deployment
