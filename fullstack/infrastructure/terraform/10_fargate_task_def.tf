# Fargate task definition for the Django API server.
resource "aws_ecs_task_definition" "api_farget_task_def" {
  requires_compatibilities = ["FARGATE"]

  family = "${local.deployment}-api-task-def"
  container_definitions = data.template_file.api_fargate_task_def.rendered

  task_role_arn = aws_iam_role.api_ecs_task_role.arn

  # This was manually created following:
  # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html#create-task-execution-role
  execution_role_arn = "arn:aws:iam::441140562335:role/ecsTaskExecutionRole"

  cpu = var.api_fargate_cpu
  memory = var.api_fargate_memory

  network_mode  = "awsvpc"

  tags = local.tags
}

# Template renderer for the Fargate task definition.
data "template_file" "api_fargate_task_def" {
  template = file("templates/fargate_task_def.json")

  vars = {
    container = local.api_container
    image = format("%s:latest", aws_ecr_repository.api.repository_url)

    fargate_cpu = var.api_fargate_cpu
    fargate_memory = var.api_fargate_memory

    cmd = jsonencode(var.api_fargate_cmd)

    port = var.api_port

    # With these two set, the API Fargate task will pull env vars from Secrets Manager.
    kv_region = var.aws_region
    kv_secret = aws_secretsmanager_secret.api_secret.id

    log_group_name = local.deployment
    log_region = var.aws_region
    log_prefix = "fargate/api/"
  }
}
