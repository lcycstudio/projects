terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 3.56.0"
      # For AWS authentication:
      # https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication
    }
  }
}

provider "aws" {
  region  = var.aws_region
}

data "aws_availability_zones" "aaz" {}
