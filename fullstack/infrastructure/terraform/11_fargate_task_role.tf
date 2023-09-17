# ECS task role for the Django API task.
resource "aws_iam_role" "api_ecs_task_role" {
  name = "${local.deployment}-ecs-task-role-api-mk2"
  assume_role_policy = data.aws_iam_policy_document.api_ecs_task_role_policy_1.json

  tags = local.tags
}

# -------------------------------------

# Assume ECS role policy for the Django API task.
data "aws_iam_policy_document" "api_ecs_task_role_policy_1" {
  version = "2012-10-17"
  statement {
    sid = ""
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# -------------------------------------

# We dropeed policy_2.

# -------------------------------------

# Attach the custom policy to the Django API task role.
resource "aws_iam_role_policy_attachment" "api_ecs_task_role_policy_3" {
  role = aws_iam_role.api_ecs_task_role.name
  policy_arn = aws_iam_policy.api_ecs_task_role_policy_3.arn
}

# Custom task policy for the Django API task.
resource "aws_iam_policy" "api_ecs_task_role_policy_3" {
  name = "${local.deployment}-fargate-task-policy-api-mk2"
  policy = data.template_file.api_ecs_task_role_policy_3.rendered
}

# Template renderer for the custom task policy for the Django API task.
data "template_file" "api_ecs_task_role_policy_3" {
  template = file("templates/fargate_task_policy.json")

  vars = {
    secretsmanager_secret = aws_secretsmanager_secret.api_secret.arn
    s3_storage = aws_s3_bucket.storage.arn
  }
}

# -------------------------------------

# FIXME - debug why farget_task_policy.json's S3 permission isn't working.
# Attach the AWS managed AmazonS3FullAccess to the Django API task execution role.
resource "aws_iam_role_policy_attachment" "api_ecs_task_role_policy_s3hack" {
  role = aws_iam_role.api_ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# -------------------------------------

# FIXME - debug why farget_task_policy.json's S3 permission isn't working.
# Attach the AWS managed AmazonS3FullAccess to the Django API task execution role.
resource "aws_iam_role_policy_attachment" "api_ecs_task_role_policy_seshack" {
  role = aws_iam_role.api_ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSESFullAccess"
}
