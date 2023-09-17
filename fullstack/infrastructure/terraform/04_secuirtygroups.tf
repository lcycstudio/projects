# Security Groups
#
# ALB <--> App (Django) <--> Data (PostgreSQL, Redis)
#
# And a Bastion security group connecting to Data.
#

module "alb_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "4.3.0"

  name = "${local.deployment}-sg-alb"
  vpc_id = module.vpc.vpc_id

  # Following this: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_with_cidr_blocks = [
    # Ingress via HTTPS from the world.
    {
      rule = "https-443-tcp"
    },
    # Ingress via HTTP from the world.
    {
      rule = "http-80-tcp"
    },
  ]

  computed_egress_with_source_security_group_id = [
    # Egress via Django port to app_security_group
    {
      from_port = var.api_port
      to_port = var.api_port
      protocol = "tcp"
      description = "django"
      source_security_group_id = module.app_security_group.security_group_id
    }
  ]
  number_of_computed_egress_with_source_security_group_id = 1

  tags = local.tags
}

module "app_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "4.3.0"

  name = "${local.deployment}-sg-app"
  vpc_id = module.vpc.vpc_id

  computed_ingress_with_source_security_group_id = [
    # Ingress via Django port from alb_security_group.
    {
      from_port = var.api_port
      to_port = var.api_port
      protocol = "tcp"
      description = "core"
      source_security_group_id = module.alb_security_group.security_group_id
    },

    # No SSH from bastion because everything on ECS/Fargate. Nothing to SSH into.
  ]
  number_of_computed_ingress_with_source_security_group_id = 1

  ingress_with_self = [
    # Ingress via all ports from others inside this security group.
    {
      rule = "all-all"
    },
  ]

  egress_with_cidr_blocks = [
    # Egress via all to the world.
    {
      rule = "all-all"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

  tags = local.tags
}

# module "data_security_group" {
#   source  = "terraform-aws-modules/security-group/aws"
#   version = "3.16.0"

#   name = "${local.deployment}-sg-data"
#   vpc_id = module.vpc.vpc_id

#   computed_ingress_with_source_security_group_id = [
#     #
#     # app_security_group
#     #

#     # Ingress via PostgreSQL port from app_security_group.
#     {
#       rule = "postgresql-tcp"
#       source_security_group_id = module.app_security_group.security_group_id
#     },

#     # Ingress via Redis port from app_security_group.
#     {
#       rule = "redis-tcp"
#       source_security_group_id = module.app_security_group.security_group_id
#     },

#     #
#     # bastion_security_group
#     #

#     # Ingress via PostgreSQL port from bastion_security_group.
#     {
#       rule = "postgresql-tcp"
#       source_security_group_id = module.bastion_security_group.security_group_id
#     },

#     # Ingress via Redis port from bastion_security_group.
#     {
#       rule = "redis-tcp"
#       source_security_group_id = module.bastion_security_group.security_group_id
#     },

#     # No SSH from bastion because all data stores are managed instances. Nothing to SSH into.
#   ]
#   number_of_computed_ingress_with_source_security_group_id = 4  # 6

#   ingress_with_self = [
#     # Ingress via all ports from others inside this security group.
#     {
#       rule = "all-all"
#     },
#   ]

#   egress_with_cidr_blocks = [
#     # Egress via all to the world.
#     {
#       rule = "all-all"
#       cidr_blocks = "0.0.0.0/0"
#     }
#   ]

#   tags = local.tags
# }

# module "bastion_security_group" {
#   source  = "terraform-aws-modules/security-group/aws"
#   version = "3.16.0"

#   name = "${local.deployment}-sg-bastion"
#   vpc_id = module.vpc.vpc_id

#   ingress_cidr_blocks = var.bastion_whitelist_cidr_blocks
#   ingress_with_cidr_blocks = [
#     # Ingress via SSH from ingress_cidr_blocks.
#     {
#       rule = "ssh-tcp"
#     }
#   ]

#   ingress_with_self = [
#     # Ingress via all ports from others inside this security group.
#     {
#       rule = "all-all"
#     },
#   ]

#   egress_with_cidr_blocks = [
#     # Egress via all to the world.
#     {
#       rule = "all-all"
#       cidr_blocks = "0.0.0.0/0"
#     }
#   ]

#   tags = local.tags
# }
