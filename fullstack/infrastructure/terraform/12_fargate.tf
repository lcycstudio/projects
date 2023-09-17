# See https://github.com/bradford-hamilton/terraform-ecs-fargate for a good example.

# ECS/Fargate cluster.
resource "aws_ecs_cluster" "fargate_cluster" {
  name = "${local.deployment}-fargate-cluster"
}

# Fargate service for the Django API server task.
resource "aws_ecs_service" "api_fargate" {
  launch_type = "FARGATE"

  cluster = aws_ecs_cluster.fargate_cluster.id
  name = "${local.deployment}-fargate-task-api"
  task_definition = aws_ecs_task_definition.api_farget_task_def.arn

  desired_count = var.api_fargate_task_count

  network_configuration {
    subnets = module.vpc.private_subnets
    security_groups = [module.app_security_group.security_group_id]
  }

  load_balancer {
    target_group_arn = module.api_alb.target_group_arns[0]  # assumes the first target.
    container_name = local.api_container
    container_port = var.api_port
  }
}
