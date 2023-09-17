# Bastion (aka Jump) server to connect the infra's private resources.
# module "bastion" {
#   source  = "terraform-aws-modules/ec2-instance/aws"
#   version = "2.15.0"

#   name = "${local.deployment}-bastion"
#   key_name = var.bastion_key_name

#   ami = var.bastion_ami_id
#   instance_type = "t3.small"
#   ebs_optimized = false
#   instance_count = 1

#   associate_public_ip_address = true
#   subnet_id = module.vpc.public_subnets[0]
#   vpc_security_group_ids = [module.bastion_security_group.this_security_group_id]

#   user_data = data.template_file.user_data.rendered

#   monitoring = false

#   tags = local.tags
# }

# # Bastion user data, mainly to get all the public keys into authorized_keys.
# data "template_file" "user_data" {
#   template =<<EOF
# #!/bin/bash

# touch "/home/ubuntu/terraform_was_here.txt"

# $${add_ssh_lines}

# sudo apt-get update
# sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -yq
# sudo reboot

# EOF

#   vars = {
#     add_ssh_lines = "${join("\n", data.template_file.add_ssh_line.*.rendered)}"
#   }
# }

# # Helper to build up authorized_keys file.
# data "template_file" "add_ssh_line" {
#   template ="echo $${public_key} >> /home/ubuntu/.ssh/authorized_keys"
#   count = length(var.bastion_other_public_keys)
#   vars = {
#     public_key = var.bastion_other_public_keys[count.index]
#   }
# }
