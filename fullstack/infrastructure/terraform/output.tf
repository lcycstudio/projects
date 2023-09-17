output "frontend_fqdn" {
  value = local.cloudfront_fqdn
}

output "api_fqdn" {
  value = local.api_fqdn
}

output "api_ecr_name" {
  value = aws_ecr_repository.api.name
}

output "api_ecr_url" {
  value = aws_ecr_repository.api.repository_url
}

# output "postgres_endpoint" {
#   value = module.postgres.this_db_instance_endpoint
# }

# output "postgres_devel_endpoint" {
#   value = module.postgres_devel.*.this_db_instance_endpoint
# }

# output "redis_endpoint" {
#   value = aws_elasticache_replication_group.redis.primary_endpoint_address
# }

# output "redis_devel_endpoint" {
#   value = aws_elasticache_replication_group.redis_devel.*.primary_endpoint_address
# }

output "s3_storage_name" {
  value = aws_s3_bucket.storage.id
}

output "s3_storage_devel_name" {
  value = aws_s3_bucket.storage_devel.*.id
}
