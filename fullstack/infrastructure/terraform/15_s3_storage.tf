# S3 bucket to hold user-uploaded files.
resource "aws_s3_bucket" "storage" {
  bucket = "${local.deployment}-storage"
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
resource "aws_s3_bucket_policy" "storage" {
  bucket = aws_s3_bucket.storage.id
  policy = data.template_file.storage_policy.rendered
}

# Template renderer for the storage S3 bucket policy.
data "template_file" "storage_policy" {
  template = file("templates/s3_storage_policy.json")

  vars = {
    s3_arn = aws_s3_bucket.storage.arn
    domain = var.domain
  }
}
