# CloudFront distribution to be the CDN for the React-based frontend SPA.
resource "aws_cloudfront_distribution" "fe" {
  enabled = true
  is_ipv6_enabled = false
  price_class = "PriceClass_100"

  aliases = local.cloudfront_fqdn  # the local is a list

  viewer_certificate {
    acm_certificate_arn = var.domain_acm_certificate_arn_fe
    ssl_support_method = "sni-only"
    minimum_protocol_version = "TLSv1.1_2016"
  }

  origin {
    domain_name = aws_s3_bucket.origin.bucket_regional_domain_name
    origin_id   = local.cloudfront_origin_id

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.fe_origin.cloudfront_access_identity_path
    }
  }

  default_root_object = "index.html"

  custom_error_response {
    error_code = 404
    response_code = 404
    response_page_path = "/index.html"  # must start with /
  }

  custom_error_response {
    error_code = 400
    response_code = 400
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 403
    response_code = 403
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 405
    response_code = 405
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 414
    response_code = 414
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 416
    response_code = 416
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 500
    response_code = 500
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 501
    response_code = 501
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 502
    response_code = 502
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 503
    response_code = 503
    response_page_path = "/error.html"
  }

  custom_error_response {
    error_code = 504
    response_code = 504
    response_page_path = "/error.html"
  }

  default_cache_behavior {
    allowed_methods = ["GET", "HEAD"]
    cached_methods = ["GET", "HEAD"]
    target_origin_id = local.cloudfront_origin_id  # specified in origin above.

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"

    # Uncomment and edit to change the defaults.
    # min_ttl = 0
    # default_ttl = 86400
    # max_ttl = 31536000
  }

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      # https://dev.maxmind.com/geoip/legacy/codes/iso3166/
      locations = [
        "CA",  # Canada
        "US",  # United States
      ]
    }
  }

  comment = "${local.deployment} (Terraform)"

  tags = local.tags
}

# CloudFront Origin Access Identity for the CloudFront Distribution.
# This connects the origin S3 bucket to the CloudFront Distribution via:
#     CloudFront Distribution <-> CloudFront Origin Access Identity <-(bucket policy)-> S3 Bucket
resource "aws_cloudfront_origin_access_identity" "fe_origin" {
  comment = "${local.deployment} (Terraform)"
}
