# 📊 Customer Satisfaction Analytics

> **Análisis avanzado de satisfacción del cliente bancario con arquitectura moderna en AWS**

Un proyecto integral para centralizar, procesar y analizar datos de atención al cliente utilizando técnicas de Big Data, Machine Learning y arquitectura de Data Lakehouse en AWS.

## 🎯 Objetivos del Proyecto

- **Centralizar** datos de atención al cliente (tickets, encuestas NPS, reviews, transcripciones)
- **Analizar** métricas de satisfacción y detectar causas de insatisfacción
- **Predecir** la satisfacción del cliente usando modelos de Machine Learning
- **Visualizar** insights a través de dashboards interactivos
- **Automatizar** el procesamiento y análisis de datos

## 🏗️ Arquitectura

### Arquitectura de Data Lakehouse en AWS

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Data Lakehouse │    │   Consumption   │
│                 │    │                  │    │                 │
│ • Simulador     │ ──▶│ Raw Data (S3)    │ ──▶│ AWS Athena      │
│ • APIs          │    │ Processed (S3)   │    │ QuickSight      │
│ • Kaggle        │    │ Curated (S3)     │    │ ML Models       │
│ • CFPB          │    │                  │    │ Notebooks       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                      ┌──────────────────┐
                      │   AWS Glue       │
                      │ • Data Catalog   │
                      │ • ETL Jobs       │
                      │ • Crawlers       │
                      └──────────────────┘
```

### Componentes Principales

- **🗂️ Data Lake**: Amazon S3 con estructura lakehouse (raw/processed/curated)
- **🔄 ETL**: AWS Glue para transformaciones y PySpark jobs
- **📊 Catalogación**: AWS Glue Data Catalog para metadatos
- **🔍 Consultas**: AWS Athena para análisis SQL ad-hoc
- **📈 Visualización**: Amazon QuickSight para dashboards
- **🧠 ML**: Modelos de satisfacción y análisis de sentimientos
- **🏗️ IaC**: Terraform para infraestructura como código

## 📁 Estructura del Proyecto

```
customer-satisfaction-analytics/
├── 📄 README.md                      # Documentación principal
├── 📋 requirements.txt               # Dependencias Python
├── 📊 data/                          # Datos del proyecto
│   ├── 🗂️ raw/                      # Datos originales
│   ├── 🔄 simulated/                # Datos sintéticos generados
│   ├── ✨ processed/                # Datos limpiados
│   └── 🌐 external/                 # Datos de APIs externas
├── 📥 ingestion/                     # Pipeline de ingesta
│   ├── 🐍 scripts/                  # Scripts Python
│   ├── ⚙️ aws_glue_jobs/            # Jobs de AWS Glue
│   └── 📋 configs/                  # Configuraciones
├── 💾 storage/                       # Configuración de almacenamiento
│   ├── 🏠 lakehouse/                # Definiciones lakehouse
│   ├── 📦 parquet_samples/          # Ejemplos Parquet
│   └── 📚 metadata_catalog/         # Catálogo de metadatos
├── ⚙️ processing/                    # Transformación de datos
│   ├── ⚡ pyspark_jobs/             # Jobs PySpark
│   ├── 🗄️ sql_transformations/      # Transformaciones SQL
│   └── 📓 notebooks/                # Jupyter Notebooks
├── 🛡️ governance/                    # Gobernanza y seguridad
│   ├── 🔒 security_policies/        # Políticas IAM
│   ├── 📋 lineage/                  # Linaje de datos
│   └── 🔐 anonymization/            # Scripts anonimización
├── 📊 analytics/                     # Análisis y visualización
│   ├── 📈 bi_reports/               # Dashboards BI
│   ├── 🧠 nlp_models/               # Modelos NLP
│   └── 🔬 exploratory/              # Análisis exploratorio
├── 🏗️ infra/                        # Infraestructura como código
│   ├── 🌍 terraform/                # Scripts Terraform
│   └── ☁️ cdk/                      # AWS CDK (opcional)
├── 🧪 tests/                        # Pruebas
│   ├── 📥 ingestion_tests/          # Tests de ingesta
│   ├── ⚙️ processing_tests/         # Tests de procesamiento
│   └── 🔗 integration_tests/        # Tests de integración
├── 📚 docs/                         # Documentación
└── 🚀 .github/workflows/            # CI/CD con GitHub Actions
```

## 🚀 Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/customer-satisfaction-analytics.git
cd customer-satisfaction-analytics
```

### 2. Configurar Entorno Python

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar AWS

```bash
# Configurar credenciales AWS
aws configure

# O usar variables de entorno
export AWS_ACCESS_KEY_ID=tu_access_key
export AWS_SECRET_ACCESS_KEY=tu_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 4. Generar Datos Sintéticos

```bash
# Generar datos de prueba
python ingestion/scripts/data_simulator.py \
    --tickets 10000 \
    --nps 5000 \
    --reviews 3000 \
    --transcripts 1000 \
    --output data/simulated
```

### 5. Desplegar Infraestructura

```bash
cd infra/terraform

# Inicializar Terraform
terraform init

# Planificar deployment
terraform plan -var="environment=dev"

# Aplicar cambios
terraform apply -var="environment=dev"
```

### 6. Subir Datos al Data Lake

```bash
# Subir datos simulados a S3
python ingestion/scripts/s3_uploader.py \
    --bucket tu-bucket-name \
    --data-dir data/simulated \
    --setup-structure \
    --create-glue-tables
```

## 📊 Datasets Incluidos

### 1. Customer Tickets (`customer_tickets`)
- **Descripción**: Tickets de atención al cliente
- **Registros**: ~10,000
- **Campos clave**: `ticket_id`, `cliente_id`, `canal`, `satisfaccion_score`, `duracion_minutos`

### 2. NPS Surveys (`nps_surveys`)
- **Descripción**: Encuestas Net Promoter Score
- **Registros**: ~5,000
- **Campos clave**: `nps_score`, `categoria_nps`, `comentario`

### 3. Customer Reviews (`customer_reviews`)
- **Descripción**: Reviews online de clientes
- **Registros**: ~3,000
- **Campos clave**: `calificacion`, `texto_review`, `plataforma`

### 4. Conversation Transcripts (`conversation_transcripts`)
- **Descripción**: Transcripciones de conversaciones
- **Registros**: ~1,000
- **Campos clave**: `transcript_texto`, `sentiment_score`, `satisfaccion_estimada`

## 🔧 Configuración

### Variables de Entorno

```bash
# AWS Configuration
export AWS_REGION=us-east-1
export DATA_BUCKET=customer-satisfaction-data-lake
export GLUE_DATABASE=customer_satisfaction_db

# Processing Configuration
export SPARK_WORKERS=2
export GLUE_WORKER_TYPE=G.1X
```

### Archivos de Configuración

- `infra/terraform/variables.tf`: Variables de infraestructura
- `ingestion/configs/`: Configuraciones de ingesta
- `processing/configs/`: Configuraciones de procesamiento

## 📈 Análisis y Métricas

### KPIs Principales

- **📊 Satisfacción Promedio**: Score promedio por canal/período
- **📈 NPS Score**: Net Promoter Score calculado
- **⏱️ Tiempo de Resolución**: Duración promedio por tipo de consulta
- **📱 Distribución por Canal**: Volumen y satisfacción por canal
- **🎯 Tasa de Resolución**: % de tickets resueltos satisfactoriamente

### Consultas SQL Ejemplo

```sql
-- Satisfacción promedio por canal
SELECT 
    canal,
    AVG(satisfaccion_score) as satisfaccion_promedio,
    COUNT(*) as total_tickets
FROM customer_tickets_processed 
WHERE year = 2024
GROUP BY canal;

-- Evolución del NPS mensual
SELECT 
    year,
    month,
    AVG(nps_score_calculado) as nps_mensual
FROM satisfaction_metrics
GROUP BY year, month
ORDER BY year, month;
```

## 🧠 Machine Learning

### Modelos Implementados

1. **🔮 Predicción de Satisfacción**
   - Algoritmo: XGBoost, Random Forest
   - Features: Canal, duración, tipo consulta, historial cliente
   - Métrica: AUC-ROC > 0.85

2. **📝 Análisis de Sentimientos**
   - Técnica: VADER, TextBlob, Transformers
   - Aplicado a: Reviews, comentarios NPS, transcripciones
   - Output: Score de sentimiento [-1, 1]

3. **🏷️ Categorización de Consultas**
   - Método: NLP con clasificación automática
   - Input: Texto de transcripciones
   - Categories: Técnico, financiero, producto, etc.

### Notebooks de Análisis

- `analytics/exploratory/eda_customer_satisfaction.ipynb`
- `analytics/nlp_models/sentiment_analysis.ipynb`
- `analytics/ml_models/satisfaction_prediction.ipynb`

## 📊 Dashboards y Visualización

### QuickSight Dashboards

1. **📈 Executive Dashboard**
   - KPIs principales
   - Tendencias temporales
   - Comparativas por canal

2. **🔍 Operational Dashboard**
   - Métricas en tiempo real
   - Alertas de satisfacción
   - Distribución de workload

3. **👥 Customer Insights**
   - Segmentación de clientes
   - Journey mapping
   - Sentiment analysis

### Acceso a Dashboards

```bash
# URL QuickSight (ejemplo)
https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/customer-satisfaction-executive
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests unitarios
pytest tests/ingestion_tests/

# Tests de integración
pytest tests/integration_tests/

# Tests de calidad de datos
python tests/data_quality_tests.py
```

### Cobertura de Tests

- ✅ Ingesta de datos
- ✅ Transformaciones ETL
- ✅ Calidad de datos
- ✅ Modelos ML
- ✅ APIs

## 🚀 CI/CD

### GitHub Actions

- **🔍 Code Quality**: Linting, formatting, security scan
- **🧪 Testing**: Unit tests, integration tests
- **🏗️ Infrastructure**: Terraform validate/plan
- **📦 Deployment**: Automated deployment to dev/staging/prod

### Pipeline Flow

```
PR Created → Code Quality → Tests → Terraform Plan → Review → Merge → Deploy
```

## 🛡️ Seguridad y Compliance

### Medidas de Seguridad

- **🔒 Cifrado**: Datos en reposo (S3) y en tránsito (TLS)
- **🛡️ IAM**: Roles y políticas de menor privilegio
- **🔐 Secrets**: AWS Secrets Manager para credenciales
- **📊 Auditoría**: CloudTrail para logging de accesos
- **🚫 Anonimización**: Scripts para protección de PII

### Compliance

- **GDPR**: Anonimización y derecho al olvido
- **SOX**: Retención de datos y auditoría
- **ISO 27001**: Gestión de seguridad de la información

## 📚 Documentación Adicional

- [🏗️ Guía de Arquitectura](docs/arquitectura.md)
- [🔧 Manual de Configuración](docs/configuracion.md)
- [📊 Diccionario de Datos](docs/diccionario_datos.md)
- [🧠 Documentación de Modelos ML](docs/modelos_ml.md)
- [🚀 Guía de Deployment](docs/deployment.md)

## 🤝 Contribuir

### Cómo Contribuir

1. Fork el repositorio
2. Crear branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código

- **Python**: PEP 8, type hints, docstrings
- **SQL**: Estilo estándar, comentarios
- **Terraform**: Documentación de variables
- **Git**: Commits convencionales

## 📞 Soporte y Contacto

### Equipo de Desarrollo

- **👨‍💼 Product Owner**: [Nombre] - product@empresa.com
- **👩‍💻 Tech Lead**: [Nombre] - tech.lead@empresa.com
- **👨‍🔬 Data Scientist**: [Nombre] - data.scientist@empresa.com
- **☁️ DevOps Engineer**: [Nombre] - devops@empresa.com

### Canales de Soporte

- **🎫 Issues**: GitHub Issues para bugs y feature requests
- **💬 Slack**: #customer-analytics para discusiones
- **📧 Email**: analytics-team@empresa.com
- **📖 Wiki**: Confluence space para documentación extendida

## 📝 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE) - ver el archivo LICENSE para detalles.

## 🙏 Agradecimientos

- **AWS**: Por la infraestructura cloud robusta
- **Apache Spark**: Por el procesamiento distribuido
- **Terraform**: Por la infraestructura como código
- **Kaggle**: Por los datasets de referencia
- **CFPB**: Por los datos públicos de quejas bancarias

---

<div align="center">

**📊 Customer Satisfaction Analytics**

*Transformando datos en insights accionables para mejorar la experiencia del cliente*

[🚀 Demo](https://demo.customer-analytics.com) • [📚 Docs](https://docs.customer-analytics.com) • [📊 Dashboards](https://dashboards.customer-analytics.com)

</div>
