# Secrets Manager secret for the Django API server.
resource "aws_secretsmanager_secret" "api_secret" {
  name = "${local.deployment}-api-${random_id.api_secret_random_id.b64_url}"
  recovery_window_in_days = 7

  tags = local.tags
}

# Need random ID component because deletion doesn't actually happen for recovery_window_in_days days.
resource "random_id" "api_secret_random_id" {
  byte_length = 8
}

# If secretsmanager_create_secret is true, create a secret containing of a JSON dict.
resource "aws_secretsmanager_secret_version" "api_secret_data" {
  secret_id = aws_secretsmanager_secret.api_secret.*.id[0]
  secret_string = jsonencode(var.api_secretsmanager_secret_data)
}
