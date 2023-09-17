# # RDS for PostgreSQL
# module "postgres" {
#   source  = "terraform-aws-modules/rds/aws"
#   version = "2.18.0"

#   identifier = "${local.deployment}-postgres"

#   engine = "postgres"
#   engine_version = "12.3"
#   family = "postgres12"
#   major_engine_version = "12"

#   instance_class = var.postgres_instance_class

#   allocated_storage = var.postgres_storage
#   storage_encrypted = false

#   port = "5432"

#   multi_az = false
#   subnet_ids = module.vpc.private_subnets
#   vpc_security_group_ids = [module.data_security_group.this_security_group_id]
#   publicly_accessible = false

#   username = var.postgres_master_user
#   password = var.postgres_master_password
#   iam_database_authentication_enabled = false

#   name = var.postgres_database  # set to "" for no initial database.
#   snapshot_identifier = var.postgres_snapshot_id  # set to "" for no source snapshot.

#   monitoring_interval = 60
#   create_monitoring_role = true
#   monitoring_role_name = "${local.deployment}-postgres-monitor"

#   # enabled_cloudwatch_logs_exports = [
#   #   "alert",
#   #   "audit",
#   #   "error",
#   #   "general",
#   #   "listener",
#   #   "slowquery",
#   #   "trace",
#   #   "postgresql",
#   #   "upgrade"
#   # ]

#   maintenance_window = "Sun:00:00-Sun:03:00"
#   backup_window      = "03:01-04:01"
#   backup_retention_period = 7
#   allow_major_version_upgrade = false
#   auto_minor_version_upgrade = false

#   skip_final_snapshot = false
#   final_snapshot_identifier = "${local.deployment}-postgres-final-snapshot"

#   apply_immediately = false

#   tags = local.tags
# }
