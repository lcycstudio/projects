# Get the existing Route 53 zone for the domain.
data "aws_route53_zone" "domain" {
  name = var.domain
  private_zone = false
}

# Alias(es) for the CloudFront distribution.
resource "aws_route53_record" "fe" {
  count = length(local.cloudfront_fqdn)
  zone_id = data.aws_route53_zone.domain.zone_id
  name = local.cloudfront_fqdn[count.index]
  type = "A"
  alias {
    name = aws_cloudfront_distribution.fe.domain_name
    zone_id = aws_cloudfront_distribution.fe.hosted_zone_id
    evaluate_target_health = false
  }

  allow_overwrite = true
}

# Alias for CloudFront distribution at root.
resource "aws_route53_record" "fe_root" {
  zone_id = data.aws_route53_zone.domain.zone_id
  name = var.domain
  type = "A"
  alias {
    name = aws_cloudfront_distribution.fe.domain_name
    zone_id = aws_cloudfront_distribution.fe.hosted_zone_id
    evaluate_target_health = false
  }

  allow_overwrite = true
}

# CNAME record for the API ALB.
resource "aws_route53_record" "api_alb" {
  zone_id = data.aws_route53_zone.domain.zone_id
  name = local.api_fqdn
  type = "CNAME"
  records = [module.api_alb.lb_dns_name]
  ttl = "300"

  allow_overwrite = true
}

# A record for the Bastion server.
# resource "aws_route53_record" "bastion" {
#   zone_id = data.aws_route53_zone.domain.zone_id
#   name = local.bastion_fqdn
#   type = "A"
#   records = module.bastion.public_ip
#   ttl = "300"

#   allow_overwrite = true
# }
