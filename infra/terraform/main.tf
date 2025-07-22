# Configuración del proveedor AWS
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables principales
variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "customer-satisfaction-analytics"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "Región AWS"
  type        = string
  default     = "us-east-1"
}

variable "data_bucket_name" {
  description = "Nombre del bucket S3 para datos"
  type        = string
  default     = "customer-satisfaction-data-lake"
}

# Configuración del proveedor AWS
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Data source para obtener la cuenta actual
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Bucket S3 principal para Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.data_bucket_name}-${var.environment}-${random_id.bucket_suffix.hex}"

  tags = {
    Name        = "Data Lake - Customer Satisfaction Analytics"
    Purpose     = "Data storage for customer satisfaction analytics"
    Layer       = "Raw, Processed, Curated"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Configuración de versionado del bucket
resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Configuración de cifrado del bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake_encryption" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# Bloquear acceso público al bucket
resource "aws_s3_bucket_public_access_block" "data_lake_pab" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Configuración de lifecycle para optimizar costos
resource "aws_s3_bucket_lifecycle_configuration" "data_lake_lifecycle" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "raw_data_lifecycle"
    status = "Enabled"

    filter {
      prefix = "raw-data/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }
  }

  rule {
    id     = "processed_data_lifecycle"
    status = "Enabled"

    filter {
      prefix = "processed-data/"
    }

    transition {
      days          = 60
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 180
      storage_class = "GLACIER"
    }
  }
}

# Base de datos Glue para catalogación
resource "aws_glue_catalog_database" "customer_satisfaction_db" {
  name        = "customer_satisfaction_db"
  description = "Base de datos para análisis de satisfacción del cliente"

  create_table_default_permission {
    permissions = ["ALL"]

    principal {
      data_lake_principal = "IAM_ALLOWED_PRINCIPALS"
    }
  }
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

# Política para que Glue acceda a S3
resource "aws_iam_role_policy" "glue_s3_policy" {
  name = "${var.project_name}-glue-s3-policy-${var.environment}"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetBucketLocation",
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:*",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

# Política de servicio AWS Glue
resource "aws_iam_role_policy_attachment" "glue_service_role" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Crawler de Glue para catalogar datos automáticamente
resource "aws_glue_crawler" "data_lake_crawler" {
  database_name = aws_glue_catalog_database.customer_satisfaction_db.name
  name          = "${var.project_name}-crawler-${var.environment}"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/raw-data/"
  }

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/processed-data/"
  }

  configuration = jsonencode({
    Version = 1.0
    CrawlerOutput = {
      Partitions = {
        AddOrUpdateBehavior = "InheritFromTable"
      }
      Tables = {
        AddOrUpdateBehavior = "MergeNewColumns"
      }
    }
  })

  schedule = "cron(0 6 * * ? *)"  # Ejecutar diariamente a las 6 AM UTC

  tags = {
    Name = "Data Lake Crawler"
  }
}

# Job de Glue para procesamiento de datos
resource "aws_glue_job" "data_processing_job" {
  name         = "${var.project_name}-processing-job-${var.environment}"
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "4.0"

  command {
    script_location = "s3://${aws_s3_bucket.data_lake.bucket}/scripts/data_processing_job.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"                     = "python"
    "--job-bookmark-option"              = "job-bookmark-enable"
    "--enable-metrics"                   = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-spark-ui"                  = "true"
    "--spark-event-logs-path"            = "s3://${aws_s3_bucket.data_lake.bucket}/logs/spark-events/"
    "--TempDir"                          = "s3://${aws_s3_bucket.data_lake.bucket}/temp/"
    "--SOURCE_BUCKET"                    = aws_s3_bucket.data_lake.bucket
    "--TARGET_BUCKET"                    = aws_s3_bucket.data_lake.bucket
  }

  max_retries = 1
  timeout     = 60  # 60 minutos

  worker_type       = "G.1X"
  number_of_workers = 2

  tags = {
    Name = "Data Processing Job"
  }
}

# Rol IAM para Athena
resource "aws_iam_role" "athena_role" {
  name = "${var.project_name}-athena-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "athena.amazonaws.com"
        }
      }
    ]
  })
}

# Bucket para resultados de Athena
resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.project_name}-athena-results-${var.environment}-${random_id.athena_suffix.hex}"

  tags = {
    Name = "Athena Query Results"
  }
}

resource "random_id" "athena_suffix" {
  byte_length = 4
}

# Configuración de cifrado para bucket de Athena
resource "aws_s3_bucket_server_side_encryption_configuration" "athena_results_encryption" {
  bucket = aws_s3_bucket.athena_results.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Bloquear acceso público al bucket de Athena
resource "aws_s3_bucket_public_access_block" "athena_results_pab" {
  bucket = aws_s3_bucket.athena_results.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Workgroup de Athena
resource "aws_athena_workgroup" "customer_satisfaction_workgroup" {
  name = "${var.project_name}-workgroup-${var.environment}"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/query-results/"

      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }

    bytes_scanned_cutoff_per_query     = 1073741824  # 1 GB
    engine_version {
      selected_engine_version = "Athena engine version 3"
    }
  }

  tags = {
    Name = "Customer Satisfaction Analytics Workgroup"
  }
}

# Bucket para logs de aplicación
resource "aws_s3_bucket" "logs_bucket" {
  bucket = "${var.project_name}-logs-${var.environment}-${random_id.logs_suffix.hex}"

  tags = {
    Name = "Application Logs"
  }
}

resource "random_id" "logs_suffix" {
  byte_length = 4
}

# Configuración de lifecycle para logs
resource "aws_s3_bucket_lifecycle_configuration" "logs_lifecycle" {
  bucket = aws_s3_bucket.logs_bucket.id

  rule {
    id     = "logs_lifecycle"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 2555  # 7 años para cumplimiento regulatorio
    }
  }
}

# Outputs para otros módulos
output "data_lake_bucket_name" {
  description = "Nombre del bucket S3 del Data Lake"
  value       = aws_s3_bucket.data_lake.bucket
}

output "data_lake_bucket_arn" {
  description = "ARN del bucket S3 del Data Lake"
  value       = aws_s3_bucket.data_lake.arn
}

output "glue_database_name" {
  description = "Nombre de la base de datos Glue"
  value       = aws_glue_catalog_database.customer_satisfaction_db.name
}

output "glue_role_arn" {
  description = "ARN del rol IAM de Glue"
  value       = aws_iam_role.glue_role.arn
}

output "athena_workgroup_name" {
  description = "Nombre del workgroup de Athena"
  value       = aws_athena_workgroup.customer_satisfaction_workgroup.name
}

output "athena_results_bucket" {
  description = "Bucket para resultados de Athena"
  value       = aws_s3_bucket.athena_results.bucket
}

output "crawler_name" {
  description = "Nombre del crawler de Glue"
  value       = aws_glue_crawler.data_lake_crawler.name
}

output "processing_job_name" {
  description = "Nombre del job de procesamiento"
  value       = aws_glue_job.data_processing_job.name
} 