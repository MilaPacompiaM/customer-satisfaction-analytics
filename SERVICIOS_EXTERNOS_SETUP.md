# 🚀 CONFIGURACIÓN PASO A PASO - SERVICIOS EXTERNOS

## 📋 **LISTA DE CUENTAS A CREAR (TODAS GRATUITAS)**

### 🎯 **RESUMEN RÁPIDO**
```
✅ AWS (YA TIENES): Account 155537880398
🆕 Streamlit Cloud: Dashboard web gratuito  
🆕 GitHub Actions: Ya lo tienes (en tu repo)
🆕 Grafana Cloud: Monitoreo y alertas
🆕 Google Colab: Machine Learning gratis
🆕 Slack/Discord: Notificaciones (opcional)
```

---

## 🚀 **PASO 1: STREAMLIT CLOUD (Dashboard Web GRATIS)**

### 📝 **Crear cuenta:**
1. Ve a: https://streamlit.io/cloud
2. **Sign up with GitHub** (usa tu cuenta GitHub existente)
3. **Plan**: Community (100% GRATIS)
4. **Límites**: Ilimitadas apps públicas, 1 app privada

### ⚙️ **Configurar app:**
```bash
📋 App Name: customer-satisfaction-dashboard
📋 Repository: MilaPacompiaM/customer-satisfaction-analytics  
📋 Branch: main
📋 Main file path: analytics/streamlit_dashboard/app.py
```

### 🔐 **Variables de entorno en Streamlit:**
```
AWS_ACCESS_KEY_ID = tu_access_key_aws
AWS_SECRET_ACCESS_KEY = tu_secret_key_aws  
AWS_DEFAULT_REGION = us-east-1
S3_DATA_BUCKET = customer-sat-analytics-155537880398-data-lake
S3_RESULTS_BUCKET = customer-sat-analytics-155537880398-athena-results
ATHENA_WORKGROUP = customer-sat-analytics-155537880398-workgroup
```

### 🌐 **URL final:**
`https://customer-satisfaction-dashboard.streamlit.app`

---

## 📊 **PASO 2: GRAFANA CLOUD (Monitoreo GRATIS)**

### 📝 **Crear cuenta:**
1. Ve a: https://grafana.com/auth/sign-up
2. **Plan**: Free (GRATIS para siempre)
3. **Límites**: 10,000 series metrics, 50GB logs, 14 días retención

### 📋 **Información de registro:**
```
✏️ Email: paradox1100p@gmail.com
✏️ Company: Analytics Team  
✏️ Stack name: customer-satisfaction-analytics
✏️ Region: US East
```

### 🔗 **Configurar datasource AWS:**
```
📋 Datasource type: Amazon Athena
📋 Region: us-east-1
📋 Workgroup: customer-sat-analytics-155537880398-workgroup
📋 Database: customer_satisfaction_db
📋 S3 Results Location: s3://customer-sat-analytics-155537880398-athena-results/
```

### 🌐 **URL del stack:**
`https://customer-satisfaction-analytics.grafana.net`

---

## 🤖 **PASO 3: GITHUB ACTIONS (YA LO TIENES)**

### ✅ **Tu repositorio ya tiene configurado:**
- `.github/workflows/data-pipeline.yml`
- Secrets configurados para AWS
- Triggers automáticos cada día

### 🔐 **Agregar secrets (si faltan):**
1. Ve a: `GitHub repo → Settings → Secrets and variables → Actions`
2. Agregar:
```
AWS_ACCESS_KEY_ID = tu_access_key
AWS_SECRET_ACCESS_KEY = tu_secret_key
NOTIFICATION_EMAIL = paradox1100p@gmail.com
```

---

## 🧠 **PASO 4: GOOGLE COLAB (Machine Learning GRATIS)**

### 📝 **Crear cuenta:**
1. Ve a: https://colab.research.google.com
2. **Sign in** con cuenta Google (crea una si no tienes)
3. **Plan**: Gratuito (GPU limitada pero suficiente)

### 📓 **Configurar notebook:**
```python
# Instalar librerías
!pip install boto3 pandas scikit-learn awswrangler

# Configurar AWS (en Colab)
import os
os.environ['AWS_ACCESS_KEY_ID'] = 'tu_access_key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'tu_secret_key'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# Conectar a tus datos
import boto3
import pandas as pd

s3 = boto3.client('s3')
bucket = 'customer-sat-analytics-155537880398-data-lake'
```

### 📁 **Notebooks incluidos:**
- `analytics/ml_models/satisfaction_predictor.ipynb`
- `analytics/nlp_models/sentiment_analyzer.ipynb`

---

## 🔔 **PASO 5: NOTIFICACIONES (OPCIONAL)**

### 📱 **Slack (GRATIS):**
1. Ve a: https://slack.com/create
2. **Workspace name**: Customer Analytics Team
3. **Channel**: #alerts, #dashboards

### 🎮 **Discord (GRATIS):**
1. Ve a: https://discord.com
2. **Server name**: Customer Analytics
3. **Channel**: #aws-alerts, #data-updates

---

## 📋 **CRONOGRAMA DE CONFIGURACIÓN**

### 🕐 **Día 1 (15 minutos):**
- ✅ Terraform apply (AWS Free Tier)
- 🆕 Crear cuenta Streamlit Cloud
- 🆕 Deploy dashboard en Streamlit

### 🕑 **Día 2 (10 minutos):**
- 🆕 Crear cuenta Grafana Cloud  
- 🆕 Configurar dashboards de monitoreo

### 🕒 **Día 3 (5 minutos):**
- 🆕 Configurar Google Colab
- 🆕 Setup notificaciones (opcional)

---

## 💰 **COSTO TOTAL MENSUAL**

```
┌─────────────────────┬─────────────┬──────────────┐
│ Servicio            │ Plan        │ Costo Mensual│
├─────────────────────┼─────────────┼──────────────┤
│ AWS Free Tier       │ Free        │ $0.00        │
│ Streamlit Cloud     │ Community   │ $0.00        │
│ GitHub Actions      │ Free        │ $0.00        │
│ Grafana Cloud       │ Free        │ $0.00        │
│ Google Colab        │ Free        │ $0.00        │
│ Slack/Discord       │ Free        │ $0.00        │
├─────────────────────┼─────────────┼──────────────┤
│ **TOTAL**           │             │ **$0.00**    │
└─────────────────────┴─────────────┴──────────────┘
```

---

## 🚀 **¿EMPEZAMOS CON EL DEPLOYMENT?**

### 📋 **Orden recomendado:**
1. **🔥 AWS Infrastructure** (terraform apply)
2. **📊 Streamlit Dashboard** (deploy en cloud)  
3. **📈 Grafana Monitoring** (setup dashboards)
4. **🧠 Google Colab ML** (notebooks de análisis)

¿Procedemos con el **terraform apply** primero? 🎯
