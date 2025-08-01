# 🚀 GUÍA DE SERVICIOS EXTERNOS - CUSTOMER SATISFACTION ANALYTICS

## 📋 **RESUMEN: SERVICIOS EXTERNOS GRATUITOS**

Esta guía te ayuda a configurar servicios externos **GRATUITOS** para reemplazar componentes costosos de AWS y mantener el proyecto en **$0.00**.

---

## 🎯 **ARQUITECTURA HÍBRIDA (AWS + SERVICIOS EXTERNOS)**

```
┌─────────────────────────────────────────────────────────┐
│                   🌐 SERVICIOS EXTERNOS                 │
├─────────────────────────────────────────────────────────┤
│  📊 Streamlit Dashboard  │  🤖 GitHub Actions          │
│  🔔 Slack/Discord        │  📈 Grafana Cloud           │
│  💾 Google Drive Backup  │  🧠 Google Colab ML         │
└─────────────────┬───────────────────────────────────────┘
                  │ (APIs / AWS SDK)
┌─────────────────▼───────────────────────────────────────┐
│                   ☁️ AWS (FREE TIER)                    │
├─────────────────────────────────────────────────────────┤
│  📦 S3 (5GB)     │  🔍 Athena (5GB)                    │
│  🔧 Glue (1M hrs) │  📊 CloudWatch (5GB)               │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 **1. DASHBOARD EXTERNO (Streamlit - GRATIS)**

### **Configuración:**
```bash
# 1. Instalar Streamlit
pip install streamlit boto3 pandas plotly

# 2. Configurar credenciales AWS
aws configure
# AWS Access Key ID: tu_access_key
# AWS Secret Access Key: tu_secret_key
# Default region: us-east-1

# 3. Ejecutar dashboard
cd analytics/streamlit_dashboard/
streamlit run app.py
```

### **Variables de entorno (.env):**
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# S3 Buckets (obtenidos de terraform output)
S3_DATA_BUCKET=customer-satisfaction-data-lake-dev-XXXXX
S3_RESULTS_BUCKET=customer-satisfaction-athena-results-dev-XXXXX

# Athena Configuration
ATHENA_WORKGROUP=customer-satisfaction-workgroup-dev
ATHENA_DATABASE=customer_satisfaction_db

# Dashboard Configuration
STREAMLIT_HOST=localhost
STREAMLIT_PORT=8501
```

### **Deploy en servicios gratuitos:**
- **Streamlit Cloud**: https://streamlit.io/cloud (GRATIS)
- **Heroku**: Free tier (550 horas/mes)
- **Railway**: $5 crédito inicial
- **Render**: 750 horas gratuitas/mes

---

## 📈 **2. GRAFANA CLOUD (GRATIS - 10K Series)**

### **Configuración:**
```bash
# 1. Crear cuenta en https://grafana.com/
# Plan Free: 10,000 series, 14 días retención

# 2. Configurar datasource Athena
# URL: https://athena.us-east-1.amazonaws.com
# Workgroup: customer-satisfaction-workgroup-dev
# Database: customer_satisfaction_db
```

### **Dashboard templates incluidos:**
- KPIs de satisfacción del cliente
- Tendencias temporales
- Análisis geográfico
- Alertas automáticas

---

## 🤖 **3. GITHUB ACTIONS (GRATIS - 2000 min/mes)**

### **Workflow para procesamiento de datos:**
```yaml
# .github/workflows/data-processing.yml
name: Data Processing Pipeline

on:
  schedule:
    - cron: '0 6 * * *'  # Diario a las 6 AM
  workflow_dispatch:      # Manual trigger

jobs:
  process-data:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install boto3 pandas awswrangler
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Run data processing
      run: |
        python scripts/data_processing.py
    
    - name: Trigger Glue Crawler
      run: |
        aws glue start-crawler --name customer-satisfaction-analytics-crawler-dev
```

---

## 🧠 **4. GOOGLE COLAB (GRATIS - GPU/TPU)**

### **Configuración para ML:**
```python
# En Google Colab
!pip install boto3 pandas scikit-learn

# Autenticación AWS
from google.colab import files
uploaded = files.upload()  # Subir credentials.csv

# Conectar a S3
import boto3
s3 = boto3.client('s3',
    aws_access_key_id='your_key',
    aws_secret_access_key='your_secret',
    region_name='us-east-1'
)

# Descargar datos
s3.download_file('your-bucket', 'processed-data/dataset.csv', 'dataset.csv')

# Entrenar modelo
# ... tu código ML ...

# Subir modelo entrenado
s3.upload_file('model.pkl', 'your-bucket', 'models/model.pkl')
```

---

## 🔔 **5. NOTIFICACIONES GRATUITAS**

### **Slack (GRATIS - 10K mensajes/mes):**
```python
import requests

def send_slack_notification(message):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    payload = {
        "text": f"🚨 Customer Analytics Alert: {message}",
        "username": "AWS-Monitor",
        "icon_emoji": ":warning:"
    }
    requests.post(webhook_url, json=payload)
```

### **Discord (GRATIS - ilimitado):**
```python
def send_discord_notification(message):
    webhook_url = "https://discord.com/api/webhooks/YOUR/WEBHOOK"
    payload = {
        "content": f"📊 **Customer Analytics**: {message}",
        "username": "AWS Monitor"
    }
    requests.post(webhook_url, json=payload)
```

---

## 💾 **6. BACKUP EXTERNO (GRATIS)**

### **Google Drive (15GB gratis):**
```python
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def backup_to_gdrive(local_file, gdrive_folder):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    
    file_drive = drive.CreateFile({
        'title': f'backup-{datetime.now().strftime("%Y%m%d")}',
        'parents': [{'id': gdrive_folder}]
    })
    file_drive.SetContentFile(local_file)
    file_drive.Upload()
```

---

## 🔧 **7. CONFIGURACIÓN COMPLETA**

### **Archivo .env completo:**
```bash
# =============================================================================
# CUSTOMER SATISFACTION ANALYTICS - EXTERNAL SERVICES CONFIG
# =============================================================================

# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# S3 Buckets (from terraform output)
S3_DATA_BUCKET=customer-satisfaction-data-lake-dev-XXXXX
S3_RESULTS_BUCKET=customer-satisfaction-athena-results-dev-XXXXX

# Athena Configuration
ATHENA_WORKGROUP=customer-satisfaction-workgroup-dev
ATHENA_DATABASE=customer_satisfaction_db

# External Services
STREAMLIT_HOST=localhost
STREAMLIT_PORT=8501

# Grafana Cloud
GRAFANA_URL=https://your-org.grafana.net
GRAFANA_API_KEY=your_api_key
GRAFANA_ORG_ID=your_org_id

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Backup
GDRIVE_CREDENTIALS_PATH=./credentials/gdrive_credentials.json
GDRIVE_FOLDER_ID=your_folder_id
```

---

## 🚀 **8. COMANDOS DE DEPLOYMENT**

### **Setup inicial:**
```bash
# 1. Crear infraestructura AWS (FREE TIER)
cd infra/terraform/
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars con tu configuración
terraform init
terraform plan
terraform apply

# 2. Configurar servicios externos
# Obtener outputs de Terraform
terraform output external_integration_config

# 3. Configurar Streamlit
cd ../../analytics/streamlit_dashboard/
pip install -r requirements.txt
streamlit run app.py

# 4. Deploy GitHub Actions
# Configurar secrets en GitHub:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# 5. Configurar Google Colab
# Usar notebook: notebooks/ml_training_colab.ipynb
```

### **Destruir infraestructura (cuando no uses):**
```bash
terraform destroy
```

---

## 💰 **COSTO TOTAL: $0.00**

| **Servicio** | **Plan Gratuito** | **Limitaciones** |
|--------------|-------------------|------------------|
| **AWS S3** | 5GB/mes | ✅ Suficiente |
| **AWS Athena** | 5GB escaneado/mes | ✅ Con límites por query |
| **AWS Glue** | 1M DPU-horas/mes | ✅ Más que suficiente |
| **Streamlit Cloud** | Gratis | ✅ Apps públicas |
| **Grafana Cloud** | 10K series/14d | ✅ Para monitoring básico |
| **GitHub Actions** | 2000 min/mes | ✅ Para ETL ligero |
| **Google Colab** | GPU/TPU gratis | ✅ Con timeouts |
| **Slack** | 10K mensajes/mes | ✅ Para alertas |

**Total: $0.00/mes** 🎉

---

## 📞 **SOPORTE Y TROUBLESHOOTING**

### **Problemas comunes:**
1. **Credenciales AWS**: Usar `aws configure`
2. **Límites Athena**: Optimizar queries con LIMIT
3. **Streamlit timeout**: Usar caché con `@st.cache_data`
4. **GitHub Actions límites**: Optimizar workflows

### **Monitoreo de costos:**
```bash
# Ejecutar monitor diario
python scripts/aws_cost_monitor.py --cleanup --email tu@email.com
```

¡Listo! Con esta configuración mantienes **$0.00** de costo mientras tienes una arquitectura completa y profesional. 🚀
