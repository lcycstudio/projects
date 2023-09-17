# *************************************
# General
# *****************

variable "aws_region" {
  type = string
  default = "us-east-2"
  description = "Deploy the infra to this AWS region."
}

variable "project" {
  type = string
  default = "lex"
  description = "The project codename."
}

variable "environment" {
  type = string
  default     = "staging"
  description = "The environment (e.g., dev, staging, beta, etc.)."
}

# *************************************
# Domain
# *****************

# Make sure this domain is on Route 53.
variable "domain" {
  type = string
  default= "lexstaging.com"
  description = "The root domain of the site. Each environment (i.e., clone of this site) requires its own domain."
}

# Make sure the ACM cert is in the same region as var.aws_region!
variable "domain_acm_certificate_arn" {
  type = string
  default = "arn:aws:acm:us-east-2:441140562335:certificate/9e983b2e-91de-472e-92da-966de0956c03"
  description = "The existing ARN of the ACM TLS certificate for var.domain in var.aws_region."
}

variable "domain_acm_certificate_arn_fe" {
  type = string
  default = "arn:aws:acm:us-east-1:441140562335:certificate/362231df-084b-49d3-ab03-dccce6a913e4"
  description = "The existing ARN of the ACM TLS certificate for var.domain in var.aws_region."
}

# *************************************
# Django API Fargate Task
# *****************

variable "api_port" {
  type = number
  default = 8080
  description = "The API port. This must sync with configuration in server.git/service/nginx.conf."
}

variable "api_fargate_cmd" {
  type = list
  default = []
  description = "The API run commmand. If empty, use the CMD in server.git/service/Dockerfile."
}

variable "api_fargate_cpu" {
  type = number
  default = 256
  description = "API's Fargate task's CPU."
}

variable "api_fargate_memory" {
  type = number
  default = 512
  description = "API's Fargate task's memory."
}

variable "api_fargate_task_count" {
  type = number
  default = 1
  description = "The number of deployed API Fargate task. As of 2020/09/03, no autoscaling. To edit this to scale up/down."
}

# *************************************
# Django API Fargate Task' Secrets (aka Environment Variables)
# *****************

variable "api_secretsmanager_secret_data" {
  type = map
  default = {}
  description = <<EOAPISSD
  Basically the API Fargate tasks's .env file. This map will get encoded into a JSON object and added to the Secrets
  Manger secret. The API task will then load/use each key of the JSON object as environment variables.
  EOAPISSD
}

# *************************************
# RDS (PostgreSQL)
# *****************

# variable "postgres_instance_class" {
#   type = string
#   default = "db.t3.small"
#   description = "VM size of the RDS PostgreSQL cluster nodes."
# }

# variable "postgres_storage" {
#   type = number
#   default = 10
#   description = "Max size in GB of the RDS PostgreSQL data."
# }

# variable "postgres_master_user" {
#   type = string
#   default = "postgres_master_user"
#   description = "Name of the RDS PostgreSQL master user."
# }

# variable "postgres_master_password" {
#   type = string
#   description = "Password of the RDS PostgreSQL master user."
# }

# Only one of postgres_database or postgres_snapshot_id should be set.
# I.e, you're creating an initial, empty database, or initiazing the DB off a snapshot.
# variable "postgres_database" {
#   type = string
#   default = ""  # no database
#   description = "If set, create a database in the RDS PostgreSQL instance with this name."
# }

# variable "postgres_snapshot_id" {
#   type = string
#   default = ""
#   description = "If set, create the RDS PostgreSQL instance as a copy of this snapshot."
# }

# *************************************
# ElastiCache (Redis)
# *****************

# variable "redis_node_type" {
#   type = string
#   default = "cache.t3.micro"
#   description = "VM size of the ElastiCache Redis cluster nodes."
# }

# variable "redis_number_cache_clusters" {
#   type = number
#   default = 1
#   description = "Number of nodes in the ElastiCache Redis cluster."
# }

# *************************************
# Storage S3
# *****************

variable "s3_storage_source_s3" {
  type = string
  default = ""
  description = "If set, copy the contents of the source S3 to the storage S3 bucket."
}

# *************************************
# Bastion Server
# *****************

# Make sure the AMI ID is from the right region.
# https://cloud-images.ubuntu.com/locator/ec2/
# variable "bastion_ami_id" {
#   type = string
#   default = "ami-0a817b0856bd5d87a"  # Ubuntu 18.04 LTS / amd64 / us-east-2
#   description = "AMI ID of the Bastion server. Use an Ubuntu LTS."
# }

# variable "bastion_key_name" {
#   type = string
#   default = "bastion_server"
#   description = "Name of the existing key name in var.region to use as the primary SSH authorized key."
# }

variable "bastion_other_public_keys" {
  type = list
  default = []
  description = "List of public SSH keys to add to the bastion server's authorized_keys list."
}

variable "bastion_whitelist_cidr_blocks" {
  type = list
  default = ["0.0.0.0/0"]
  description = "IP whitelist to access to the bastion server. Use CIDR notation ($ip/32)."
}

# *************************************
# Development
# *****************

variable "devel_enabled" {
  type = bool
  default = false
  description = "Enable to create development RDS (PostgreSQL), ElastiCache (Redis), and storage S3."
}
