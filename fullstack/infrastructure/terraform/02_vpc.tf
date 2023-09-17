# VPC for the deployment.
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.66.0"

  name = "${local.deployment}-vpc"
  cidr = "10.0.0.0/16"

  azs = data.aws_availability_zones.aaz.names
  public_subnets = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  # Single NAT gateway for all private subnets.
  enable_nat_gateway = true
  single_nat_gateway = true
  one_nat_gateway_per_az = false

  enable_dns_hostnames = true
  enable_dns_support = true

  tags = local.tags
}
