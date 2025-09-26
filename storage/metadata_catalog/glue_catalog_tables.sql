-- AWS Glue Catalog Table Definitions
-- Customer Satisfaction Analytics Data Lake

-- Raw Layer Tables
CREATE EXTERNAL TABLE raw_customer_tickets (
    ticket_id STRING,
    customer_id STRING,
    channel STRING,
    department STRING,
    issue_type STRING,
    satisfaction_score INT,
    created_at STRING,
    resolved_at STRING,
    duration_minutes INT,
    agent_id STRING,
    priority STRING,
    status STRING
)
STORED AS PARQUET
LOCATION 's3://customer-satisfaction-raw/tickets/'
TBLPROPERTIES (
    'classification'='parquet',
    'compressionType'='snappy'
);

CREATE EXTERNAL TABLE raw_nps_surveys (
    survey_id STRING,
    customer_id STRING,
    ticket_id STRING,
    nps_score INT,
    promoter_type STRING,
    feedback_text STRING,
    survey_date STRING,
    channel STRING
)
STORED AS PARQUET
LOCATION 's3://customer-satisfaction-raw/nps_surveys/'
TBLPROPERTIES (
    'classification'='parquet',
    'compressionType'='snappy'
);

-- Processed Layer Tables (Delta Lake)
CREATE TABLE processed_customer_interactions (
    interaction_id STRING,
    customer_id_hash STRING,
    channel STRING,
    department STRING,
    satisfaction_score INT,
    sentiment STRING,
    interaction_date DATE,
    resolution_time_hours DOUBLE,
    first_contact_resolution BOOLEAN
)
USING DELTA
LOCATION 's3://customer-satisfaction-processed/interactions/'
PARTITIONED BY (year(interaction_date), month(interaction_date));

-- Curated Layer Tables (Analytics Ready)
CREATE TABLE curated_satisfaction_metrics (
    date_key DATE,
    channel STRING,
    department STRING,
    avg_satisfaction DOUBLE,
    nps_score DOUBLE,
    total_interactions BIGINT,
    resolution_rate DOUBLE,
    escalation_rate DOUBLE
)
USING DELTA
LOCATION 's3://customer-satisfaction-curated/metrics/'
PARTITIONED BY (year(date_key), month(date_key));

-- Data Quality Monitoring
CREATE TABLE data_quality_metrics (
    table_name STRING,
    check_date DATE,
    completeness_score DOUBLE,
    consistency_score DOUBLE,
    validity_score DOUBLE,
    total_records BIGINT,
    failed_records BIGINT
)
USING DELTA
LOCATION 's3://customer-satisfaction-curated/data_quality/';