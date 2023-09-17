#!/usr/bin/env bash
#
# Exports a Route 53 hosted zone records to a file. Recommend doing this prior
# to any changes to a hosted zone.
#
# This script assumes you have the AWS CLI v2 installed, and it has been
# configured with IAM credentials to read the hosted zone in question.
#
set -e

readonly environment=${1:-"staging"}

# staging = serverstaging.com
# live = myproject.com
declare -A zone_id=(\
    ["staging"]="Z0410203KPUC3LAVCWKU"\
    ["live"]="ZMJXIDT9ZNR5V"\
)

aws route53 list-resource-record-sets --hosted-zone-id "${zone_id[$environment]}" > "server_aws_r53_${environment}.txt"
