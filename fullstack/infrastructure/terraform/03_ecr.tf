# Elastic Container Registry (ECR) for the Django API server.
resource "aws_ecr_repository" "api" {
  name = "${local.deployment}-ecr-api"

  tags = local.tags
}

# ECR lifecycle policy to dictate how long to keep untagged images.
resource "aws_ecr_lifecycle_policy" "api" {
  repository = aws_ecr_repository.api.name
  policy = <<POLICY
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Expire untagged images older than 7 days.",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
  POLICY
}
