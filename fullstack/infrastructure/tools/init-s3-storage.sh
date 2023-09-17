#!/usr/bin/env bash
#
# Initialize the S3 storage bucket with the contents of a "source" S3 bucket.
#
# Normally would do this in Terraform as a "null_resource," but we're using
# Terraform Cloud, and I can't figure out how to add the AWS CLI to that.
#
# If you can, or we go back to using the Terraform CLI, then see this:
#
# https://stackoverflow.com/questions/62801569/can-terraform-duplicate-the-content-of-an-s3-bucket
#
# This script assumes you have the AWS CLI v2 installed, and it has been
# configured with IAM credentials with at least read access to the source and
# read/write access to the destination S3 buckets.
#
set -e

readonly src_bucket="$1"
readonly dst_bucket="$2"

read -p "Sync from s3://$src_bucket to s3://$dst_bucket? [Y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Y]$ ]]
then
    echo "Aborted!"
    exit 1
fi

aws s3 sync --acl "private" "s3://$src_bucket" "s3://$dst_bucket"
