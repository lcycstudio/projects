# S3 bucket to hold user-uploaded files.
resource "aws_s3_bucket" "storage_devel" {
  count = var.devel_enabled ? 1 : 0

  bucket = "${local.deployment}-storage-devel"
  acl = "private"
  force_destroy = false

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = [
      "http://*.${var.domain}",
      "https://*.${var.domain}",
      "http://localhost",
      "http://*.localhost"
    ]
  }

  tags = local.tags
}

# S3 bucket policy to allow public read from the domain and localhost.
resource "aws_s3_bucket_policy" "storage_devel" {
  count = var.devel_enabled ? 1 : 0

  bucket = aws_s3_bucket.storage_devel.0.id
  policy = data.template_file.storage_policy_devel.0.rendered
}

# Template renderer for the storage S3 bucket policy.
data "template_file" "storage_policy_devel" {
  count = var.devel_enabled ? 1 : 0

  template = file("templates/s3_storage_policy.json")

  vars = {
    s3_arn = aws_s3_bucket.storage_devel.0.arn
    domain = var.domain
  }
}
