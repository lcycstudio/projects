locals {
  deployment = "${var.project}-${var.environment}"
  api_container = "${var.project}-${var.environment}-api-container"
  api_fqdn = "${var.environment}-api.${var.domain}"
  bastion_fqdn = "${var.environment}-bst.${var.domain}"
  cloudfront_fqdn = [var.domain, "*.${var.domain}"]
  cloudfront_origin_id = "${var.project}-${var.environment}-s3origin"
  s3_origin = "${var.environment}.${var.domain}"
  tags =  {
    project = var.project
    environment = var.environment
    manager = "Terraform"
  }
}
