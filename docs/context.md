# Análisis de Satisfacción del Cliente

## Información General

Los datos de atención al cliente incluyen encuestas de satisfacción y registros de interacción (llamadas, chats, e-mails).

### Fuentes de Datos Disponibles

#### Datasets Públicos
- **Kaggle - Santander Customer Satisfaction**: Dataset con cientos de variables anónimas de clientes y campo TARGET (1=insatisfecho)
- **Kaggle - Bank Customer Reviews**: ~1,000 reseñas de usuarios de diversos bancos (autor, fecha, banco, calificación 1–5, texto)
- **CFPB - Consumer Complaint Database**: Base de quejas de consumidores en EE.UU. (incluye "Bank Accounts", "Credit Cards", etc.)

#### Simulación de Datos (Recomendada)
Crear datos sintéticos de encuestas o tickets de soporte con las siguientes características:

**Variables de Tickets de Servicio:**
- TicketID, Fecha, ClienteID, Canal (teléfono/chat/email)
- Duración, Departamento, Resultado, Satisfacción (1–5)
- Transcripciones de conversación (opcional)

**Variables de Encuestas:**
- EncuestaID, Fecha, ClienteID, SucursalID
- Puntuación, Comentario, AsesorID, InteracciónID
- Canal, TiempoRespuesta, Estado

**Herramientas:**
- Python + Faker para datos básicos
- Modelos generativos (GPT) para texto
- Técnicas de NLP para textos ficticios

**Volumen:** Decenas de miles de interacciones por canal anual

## Objetivos del Proyecto

### Problemática a Resolver
Desarrollar el sentido de la oportunidad de negocio, demostrando conocimiento profundo del problema y capacidad para proponer mejoras.

### Propuesta de Solución
Crear una arquitectura moderna en AWS que permita:

1. **Centralización de Datos**: Integrar datos de atención al cliente (chats, llamadas, emails, reseñas)
2. **Análisis de Métricas**: Analizar satisfacción y detectar causas de insatisfacción
3. **Exposición de Resultados**: Dashboards, consultas SQL y modelos ML

## Distribución de Tareas

### Opción 1: Por Etapas

#### Persona 1 - Arquitectura y Seguridad
- **Servicios AWS**: Selección para almacenamiento, procesamiento y consumo
- **Data Lakehouse**: Diseño con S3 + Glue + Athena + Redshift Serverless
- **Seguridad**: Encriptación, IAM, permisos, anonimización
- **Estándares**: ISO 27001, GDPR, CCPA

#### Persona 2 - Ingesta y Simulación de Datos
- **Simulación con Python + Faker**:
  - Tickets de atención (TicketID, Canal, Fecha, Satisfacción)
  - Transcripciones sintéticas con LLMs (opcional)
  - Encuestas tipo NPS, reviews (texto)
- **Automatización**: Scripts para generar miles de datos diarios
- **Carga**: Subir datos crudos al Raw Layer en S3 (Parquet/CSV)

#### Persona 3 - Procesamiento y Analítica
- **ETL con AWS Glue/PySpark**:
  - Limpieza, transformación y anonimización
  - Enriquecimiento de variables
  - Almacenamiento en Delta Lake/Iceberg
- **Modelos Analíticos**: Por canal, duración, satisfacción promedio
- **Vistas**: Para consumo BI y ML

#### Persona 4 - Consumo y Visualización
- **Dashboards**: QuickSight o Power BI (conexión Redshift/Athena)
- **KPIs SQL**:
  - % clientes insatisfechos por canal
  - Duración promedio por resultado
  - Reviews con sentimiento negativo
- **ML**: Modelo para predecir insatisfacción (clasificación binaria)


### Opción 2: Por Roles

| Integrante | Rol Principal | Responsabilidades |
|------------|---------------|-------------------|
| **Persona 1** | Líder de Ingesta y Simulación | • Diseñar esquemas de datos simulados<br>• Generar scripts Python con Faker/GPT<br>• Implementar ingesta en AWS S3/Kinesis |
| **Persona 2** | Líder de Almacenamiento y Catalogación | • Estructura Data Lake (S3) y Delta Lake<br>• Glue Data Catalog<br>• Versionado y particionado |
| **Persona 3** | Líder de Procesamiento y ML | • Procesamiento EMR/Glue con PySpark<br>• Pipeline ML (modelo satisfacción)<br>• Limpieza, preparación y entrenamiento |
| **Persona 4** | Líder de Seguridad y Consumo | • Gestión IAM, cifrado, anonimización<br>• Acceso BI (Athena/QuickSight)<br>• Dashboard exploratorio |


## Estructura del Repositorio

```
customer-satisfaction-analytics/
│
├── README.md                      # Documentación principal del proyecto
├── requirements.txt              # Dependencias del proyecto (Python, AWS SDK, etc.)
├── .gitignore                    # Ignorar archivos innecesarios como __pycache__
├── LICENSE                       # Tipo de licencia (ej. MIT)
│
├── data/                         # Datos simulados, crudos y procesados
│   ├── raw/                      # Datos originales (ej. CSV de Kaggle, CFPB)
│   ├── simulated/               # Datos simulados con Faker o GPT
│   ├── processed/               # Datos limpios/listos para análisis o ingesta
│   └── external/                # Datos descargados de APIs o datasets de terceros
│
├── ingestion/                   # Pipelines de ingesta de datos
│   ├── scripts/                 # Scripts Python de ingesta
│   ├── aws_glue_jobs/           # Código de Glue jobs, Glue triggers, crawlers
│   └── configs/                 # Configs YAML/JSON de Glue o conectores
│
├── storage/                     # Configuración de almacenamiento
│   ├── lakehouse/               # Estructura del Lakehouse (Delta Lake, Iceberg)
│   ├── parquet_samples/         # Ejemplos de Parquet generados
│   └── metadata_catalog/        # Glue catalog definitions
│
├── processing/                  # Transformaciones y limpieza
│   ├── pyspark_jobs/            # Transformaciones con PySpark
│   ├── sql_transformations/     # SQLs sobre Athena o Redshift Spectrum
│   └── notebooks/               # Jupyter o SageMaker Notebooks
│
├── governance/                  # Políticas y gobernanza
│   ├── security_policies/       # IAM Roles, Secrets Manager, permisos
│   ├── lineage/                 # Lineaje de datos (ej. AWS Data Lineage o Atlas)
│   └── anonymization/           # Scripts de anonimización y hashing
│
├── analytics/                   # Análisis de datos y visualización
│   ├── bi_reports/              # Dashboards (ej. Power BI, QuickSight, Streamlit)
│   ├── nlp_models/              # Modelos ML/NLP entrenados
│   └── exploratory/             # Análisis exploratorios
│
├── infra/                       # Infraestructura como código
│   ├── terraform/               # Scripts Terraform para AWS
│   └── cdk/                     # Opcional: AWS CDK (Python)
│
├── tests/                       # Pruebas unitarias, integración y validación
│   └── ingestion_tests/
│
├── docs/                        # Documentación adicional
│   ├── arquitectura.png         # Diagrama de arquitectura
│   └── presentacion_equipo.pdf  # Presentación para el diplomado
│
└── .github/                     # Configuración para GitHub Actions u otros CI/CD
    └── workflows/
```
