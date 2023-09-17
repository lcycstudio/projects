#!/usr/bin/env bash
#
# Restarts the Fargate API cluster using the latest API image. Use this when
# you need to restart the Fargate cluster without an updated API image in the
# ECR.
#
set -e

readonly environment=${1:-staging}
readonly region="us-east-1"

declare -A ecs_cluster_name=(\
    ["staging"]="server-staging-fargate-cluster"\
    ["live"]="server-live-fargate-cluster"\
)

declare -A ecs_service_name=(\
    ["staging"]="server-staging-fargate-task-api"\
    ["live"]="server-live-fargate-task-api"\
)

aws ecs update-service --cluster "${ecs_cluster_name[$environment]}" --service "${ecs_service_name[$environment]}" --force-new-deployment --region "$region"
