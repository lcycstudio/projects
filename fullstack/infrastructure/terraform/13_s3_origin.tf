# Origin S3 bucket for the CloudFront Distribution.
resource "aws_s3_bucket" "origin" {
  bucket = local.s3_origin
  acl = "private"
  force_destroy = true

  website {
    index_document = "index.html"
    error_document = "index.html"  # TODO - create error page and add here.
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]  # sync with CloudFront.
    allowed_origins = [
      "https://${var.domain}",
      "https://*.${var.domain}"]
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
          # Cannot be KMS.
          sse_algorithm = "AES256"
      }
    }
  }

  tags = local.tags
}

# IAM policy which gives the CloudFront Orgin Access Identity access to the S3
# bucket.
data "aws_iam_policy_document" "origin" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.origin.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.fe_origin.iam_arn]
    }
  }

  statement {
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.origin.arn]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.fe_origin.iam_arn]
    }
  }
}

# Apply the IAM policy to the S3 origin bucket.
resource "aws_s3_bucket_policy" "origin" {
  bucket = aws_s3_bucket.origin.id
  policy = data.aws_iam_policy_document.origin.json
}
