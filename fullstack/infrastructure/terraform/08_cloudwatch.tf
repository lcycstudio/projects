# CloudWatch log group to receive any logs from other resources.
# Primarily for the Django API Fargate task logs.
resource "aws_cloudwatch_log_group" "cloudwatch_log_group" {
  name = local.deployment
  retention_in_days = 30

  tags = local.tags
}
