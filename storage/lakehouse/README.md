# Data Lakehouse Structure

## Arquitectura de Capas

### Raw Layer (Bronze)
- **Ubicación**: `s3://customer-satisfaction-raw/`
- **Formato**: CSV, JSON, Parquet
- **Datos**: Información cruda sin procesar
- **Retención**: 90 días, después S3 Glacier

### Processed Layer (Silver)
- **Ubicación**: `s3://customer-satisfaction-processed/`
- **Formato**: Delta Lake, Parquet optimizado
- **Datos**: Limpios, validados, anonimizados
- **Retención**: 180 días

### Curated Layer (Gold)
- **Ubicación**: `s3://customer-satisfaction-curated/`
- **Formato**: Delta Lake con optimizaciones
- **Datos**: Agregados, modelos analíticos, métricas
- **Retención**: Indefinida

## Particionado

```
/year=2024/month=03/day=15/hour=14/
```

## Esquemas

### customer_tickets
```sql
CREATE TABLE customer_tickets (
    ticket_id STRING,
    customer_id STRING,
    channel STRING,
    department STRING,
    satisfaction_score INT,
    created_at TIMESTAMP,
    resolved_at TIMESTAMP
) USING DELTA
PARTITIONED BY (year, month, day)
```

### nps_surveys
```sql
CREATE TABLE nps_surveys (
    survey_id STRING,
    customer_id STRING,
    nps_score INT,
    sentiment STRING,
    created_at TIMESTAMP
) USING DELTA
PARTITIONED BY (year, month)
```