import json
import os
import boto3

def load_env_from_aws_if_configured():
    aws_secret = os.environ.get("CORE_AWS_SECRET")
    aws_region = os.environ.get("CORE_AWS_REGION")

    if aws_secret is None or aws_region is None:
        return

    secrets_manager = boto3.client("secretsmanager", region_name=aws_region)
    response = secrets_manager.get_secret_value(SecretId=aws_secret)
    parsed_response = json.loads(response["SecretString"])

    for key, value in parsed_response.items():
        os.environ[key] = value
