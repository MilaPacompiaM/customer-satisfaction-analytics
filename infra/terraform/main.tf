# Terraform mínimo y funcional para Customer Satisfaction Analytics
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

# Provider AWS
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      Owner       = var.notification_email
      ManagedBy   = "Terraform"
      Account     = var.aws_account_id
    }
  }
}

# Random IDs para buckets únicos
resource "random_id" "data_lake_suffix" {
  byte_length = 4
}

resource "random_id" "athena_suffix" {
  byte_length = 4
}

resource "random_id" "logs_suffix" {
  byte_length = 4
}

# S3 Bucket para Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}-${random_id.data_lake_suffix.hex}"
  
  # Proteger contra eliminación accidental
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake_encryption" {
  bucket = aws_s3_bucket.data_lake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 Bucket para resultados de Athena
resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.project_name}-athena-results-${var.environment}-${random_id.athena_suffix.hex}"
  
  # Proteger contra eliminación accidental  
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "athena_results_versioning" {
  bucket = aws_s3_bucket.athena_results.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket para logs
resource "aws_s3_bucket" "logs" {
  bucket = "${var.project_name}-logs-${var.environment}-${random_id.logs_suffix.hex}"
}

# Lifecycle para logs (auto-cleanup)
resource "aws_s3_bucket_lifecycle_configuration" "logs_lifecycle" {
  bucket = aws_s3_bucket.logs.id

  rule {
    id     = "logs_cleanup"
    status = "Enabled"
    
    filter {
      prefix = ""
    }

    expiration {
      days = 30  # Eliminar logs después de 30 días para mantener costos bajos
    }
  }
}

# Base de datos Glue
resource "aws_glue_catalog_database" "customer_satisfaction_db" {
  name        = var.glue_database_name
  description = "Base de datos para análisis de satisfacción del cliente"
}

# Rol IAM para Glue
resource "aws_iam_role" "glue_role" {
  name = "${var.project_name}-glue-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service_role" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "glue_s3_policy" {
  name = "glue-s3-access"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      }
    ]
  })
}

# Athena Workgroup
resource "aws_athena_workgroup" "customer_satisfaction" {
  name = "${var.project_name}-workgroup-${var.environment}"

  configuration {
    enforce_workgroup_configuration = true
    bytes_scanned_cutoff_per_query  = 1073741824  # 1GB limit

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/"
    }
  }
}

# Budget para control de costos
resource "aws_budgets_budget" "cost_control" {
  name         = "${var.project_name}-budget-${var.environment}"
  budget_type  = "COST"
  limit_amount = tostring(var.budget_amount)
  limit_unit   = "USD"
  time_unit    = var.budget_time_unit

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = [var.notification_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 100
    threshold_type            = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.notification_email]
  }
}

# Outputs
output "data_lake_bucket_name" {
  description = "Nombre del bucket S3 para data lake"
  value       = aws_s3_bucket.data_lake.bucket
}

output "athena_results_bucket_name" {
  description = "Nombre del bucket S3 para resultados de Athena"
  value       = aws_s3_bucket.athena_results.bucket
}

output "logs_bucket_name" {
  description = "Nombre del bucket S3 para logs"
  value       = aws_s3_bucket.logs.bucket
}

output "glue_database_name" {
  description = "Nombre de la base de datos Glue"
  value       = aws_glue_catalog_database.customer_satisfaction_db.name
}

output "athena_workgroup_name" {
  description = "Nombre del workgroup de Athena"
  value       = aws_athena_workgroup.customer_satisfaction.name
}

output "total_estimated_monthly_cost" {
  description = "Costo estimado mensual (debería ser $0.00 con Free Tier)"
  value       = "$0.00 (Free Tier)"
}
