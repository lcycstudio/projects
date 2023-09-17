# API server application load balancer (ALB)
module "api_alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "6.5.0"

  load_balancer_type = "application"

  name = "${local.deployment}-alb-api"

  vpc_id = module.vpc.vpc_id
  subnets = module.vpc.public_subnets
  security_groups = [module.alb_security_group.security_group_id]

  # The Django server will register itself with this target.
  target_groups = [
    {
      name = "${local.deployment}-tg-api"
      backend_protocol = "HTTP"
      backend_port = var.api_port
      target_type = "ip"

      health_check = {
        enabled = true
        path = "/service-check/"
        protocol = "HTTP"
        matcher = "200"
        interval = 30
        health_threshold = 3
        unhealthy_threshold = 3
        timeout = 5
      }

      stickiness = {
        type = "lb_cookie"
        enabled = false
      }
    }
  ]

  https_listeners =  [
    {
      port = 443
      protocol = "HTTPS"
      certificate_arn = var.domain_acm_certificate_arn
      target_group_index = 0
    }
  ]

  tags = local.tags
}

# Redirect HTTP to HTTPs at the ALB level.
resource "aws_lb_listener" "api_alb_redirect" {
  load_balancer_arn = module.api_alb.lb_arn
  port = "80"
  protocol = "HTTP"

  default_action {
    target_group_arn = module.api_alb.target_group_arns[0]  # works because core_alb has 1 target group.
    type = "redirect"
    redirect {
      port = "443"
      protocol = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}
