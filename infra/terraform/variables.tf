# Variables principales del proyecto
variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "customer-satisfaction-analytics"
  
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "El nombre del proyecto debe contener solo letras minúsculas, números y guiones."
  }
}

variable "environment" {
  description = "Ambiente de deployment (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "El ambiente debe ser dev, staging o prod."
  }
}

variable "aws_region" {
  description = "Región AWS donde se deployarán los recursos"
  type        = string
  default     = "us-east-1"
}

# Variables para S3
variable "data_bucket_name" {
  description = "Nombre base del bucket S3 para el Data Lake"
  type        = string
  default     = "customer-satisfaction-data-lake"
}

variable "enable_versioning" {
  description = "Habilitar versionado en el bucket S3"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Habilitar cifrado en el bucket S3"
  type        = bool
  default     = true
}

# Variables para AWS Glue
variable "glue_database_name" {
  description = "Nombre de la base de datos en AWS Glue Data Catalog"
  type        = string
  default     = "customer_satisfaction_db"
}

variable "crawler_schedule" {
  description = "Programación del crawler (formato cron)"
  type        = string
  default     = "cron(0 6 * * ? *)"  # Diariamente a las 6 AM UTC
}

variable "glue_job_timeout" {
  description = "Timeout en minutos para jobs de Glue"
  type        = number
  default     = 60
}

variable "glue_worker_type" {
  description = "Tipo de worker para jobs de Glue (G.1X, G.2X, G.025X)"
  type        = string
  default     = "G.1X"
  
  validation {
    condition     = contains(["G.025X", "G.1X", "G.2X"], var.glue_worker_type)
    error_message = "Worker type debe ser G.025X, G.1X o G.2X."
  }
}

variable "glue_number_of_workers" {
  description = "Número de workers para jobs de Glue"
  type        = number
  default     = 2
}

# Variables para Athena
variable "athena_bytes_scanned_cutoff" {
  description = "Límite de bytes escaneados por consulta en Athena (en bytes)"
  type        = number
  default     = 1073741824  # 1 GB
}

# Variables para lifecycle de S3
variable "raw_data_ia_transition_days" {
  description = "Días para transición de raw data a IA"
  type        = number
  default     = 30
}

variable "raw_data_glacier_transition_days" {
  description = "Días para transición de raw data a Glacier"
  type        = number
  default     = 90
}

variable "raw_data_deep_archive_transition_days" {
  description = "Días para transición de raw data a Deep Archive"
  type        = number
  default     = 365
}

variable "processed_data_ia_transition_days" {
  description = "Días para transición de processed data a IA"
  type        = number
  default     = 60
}

variable "processed_data_glacier_transition_days" {
  description = "Días para transición de processed data a Glacier"
  type        = number
  default     = 180
}

variable "logs_retention_days" {
  description = "Días de retención para logs"
  type        = number
  default     = 2555  # 7 años para cumplimiento
}

# Variables para etiquetado
variable "additional_tags" {
  description = "Tags adicionales para aplicar a todos los recursos"
  type        = map(string)
  default     = {}
}

variable "cost_center" {
  description = "Centro de costos para billing"
  type        = string
  default     = "analytics"
}

variable "owner" {
  description = "Propietario del proyecto"
  type        = string
  default     = "data-team"
}

# Variables para configuración de red (para futuras extensiones)
variable "vpc_cidr" {
  description = "CIDR block para VPC (si se requiere VPC personalizada)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "enable_vpc_endpoints" {
  description = "Habilitar VPC endpoints para servicios AWS"
  type        = bool
  default     = false
}

# Variables para monitoring y alertas
variable "enable_cloudwatch_alarms" {
  description = "Habilitar alarmas de CloudWatch"
  type        = bool
  default     = true
}

variable "notification_email" {
  description = "Email para notificaciones de alarmas"
  type        = string
  default     = ""
}

# Variables para backup y disaster recovery
variable "enable_cross_region_replication" {
  description = "Habilitar replicación cross-region"
  type        = bool
  default     = false
}

variable "backup_retention_days" {
  description = "Días de retención para backups"
  type        = number
  default     = 30
} 