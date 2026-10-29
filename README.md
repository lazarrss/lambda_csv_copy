# Lambda CSV Copy — Serverless S3 Pipeline with AWS CDK

An **infrastructure-as-code** project built with **AWS CDK in Python**. It deploys an event-driven, serverless pipeline that automatically copies every CSV file uploaded to a source S3 bucket into a destination bucket.

## Architecture

```
CSV upload ──► S3 source bucket ──(ObjectCreated, *.csv)──► Lambda (Docker image) ──► S3 destination bucket /processed/
```

The CDK stack (`lambda_csv_copy/lambda_csv_copy_stack.py`) defines:

- **Two S3 buckets** (source and destination) with automatic cleanup on stack deletion
- A **Lambda function packaged as a Docker container image** (`lambda_src/`, based on the AWS Python 3.11 Lambda image)
- An **S3 event notification** that triggers the Lambda only for `.csv` files
- **Least-privilege IAM permissions**: read-only access to the source bucket, write-only access to the destination bucket
- **Stack outputs** with the generated bucket names

The repository also includes a **Lambda layer** experiment (`layer_src/`, `layer_demo_src/`): a ZIP-packaged function that imports `python-dateutil` from a shared layer instead of bundling it. It is commented out in the stack and can be enabled by uncommenting it.

## Project Structure

| Path | Description |
|---|---|
| `app.py` | CDK app entry point |
| `lambda_csv_copy/` | CDK stack definition |
| `lambda_src/` | Lambda handler and Dockerfile |
| `layer_src/`, `layer_demo_src/` | Lambda layer and demo function |
| `tests/` | Stack test scaffold (CDK assertions, pytest) |

## Deploying

Requirements: Python 3.11+, Node.js, the AWS CDK CLI (`npm install -g aws-cdk`), Docker and configured AWS credentials.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install aws-cdk-lib constructs
cdk bootstrap                    # first time only
cdk synth
cdk deploy
```

Remove all resources with `cdk destroy`.

## Tech Stack

Python · AWS CDK · AWS Lambda · Amazon S3 · IAM · CloudFormation · Docker
