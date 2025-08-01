# 🚀 **Guía Completa de Deployment**

> **Paso a paso para hacer funcionar el proyecto completo con costo $0.00**

---

## 📋 **Prerequisitos**

### **�️ Software Requerido**
```bash
# Verificar que tienes instalado:
python --version     # Python 3.9+
aws --version        # AWS CLI 2.0+
terraform --version  # Terraform 1.0+
docker --version     # Docker 20.0+ (opcional)
git --version        # Git 2.0+
```

### **� Cuentas Necesarias**
- ✅ **AWS Account** (Free Tier activo)
- ✅ **GitHub Account** (para Actions)
- ✅ **Streamlit Account** (gratis)
- ✅ **Google Account** (para Colab)
- ✅ **Slack Workspace** (opcional, para alertas)

---

## 🎯 **PASO 1: Setup Inicial**

### **1.1 Clonar el Repositorio**
```bash
git clone https://github.com/MilaPacompiaM/customer-satisfaction-analytics.git
cd customer-satisfaction-analytics
```

### **1.2 Configurar Python Environment**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### **1.3 Configurar AWS CLI**
```bash
aws configure

# Información requerida:
# AWS Access Key ID: [Tu Access Key]
# AWS Secret Access Key: [Tu Secret Key]  
# Default region name: us-east-1
# Default output format: json
```

**⚠️ IMPORTANTE**: Usa un usuario IAM con permisos limitados, no el root account.

---

## 🔧 **PASO 2: Configurar Variables**

### **2.1 Copiar Archivo de Configuración**
```bash
cd infra/terraform/
cp terraform.tfvars.example terraform.tfvars
```

### **2.2 Editar terraform.tfvars**
```hcl
# ============================================================================
# CONFIGURACIÓN PRINCIPAL - PERSONALIZAR AQUÍ
# ============================================================================

# 🏢 INFORMACIÓN DEL PROYECTO
project_name = "customer-satisfaction-analytics"
environment  = "dev"  # o "prod"
owner_email  = "TU-EMAIL@ejemplo.com"  # ⚠️ CAMBIAR AQUÍ

# 🌍 CONFIGURACIÓN AWS
aws_region = "us-east-1"  # Región más barata para Free Tier

# 💰 PROTECCIÓN DE COSTOS
budget_amount = 1.00  # Alerta si supera $1.00
alert_email   = "TU-EMAIL@ejemplo.com"  # ⚠️ CAMBIAR AQUÍ

# 📊 CONFIGURACIÓN SERVICIOS EXTERNOS
external_dashboard_provider = "streamlit"
external_data_processor    = "github_actions"
external_ml_platform       = "google_colab"
external_notification_channel = "slack"

# 💬 NOTIFICACIONES (Opcional)
slack_webhook_url = "https://hooks.slack.com/services/TU/WEBHOOK/URL"  # Opcional
discord_webhook_url = ""  # Opcional
telegram_bot_token = ""   # Opcional

# 🏷️ TAGS
tags = {
  Project     = "CustomerSatisfactionAnalytics"
  Environment = "dev"
  Owner       = "DataTeam"
  Cost        = "Zero"
}
```

### **2.3 Configurar Secrets (GitHub Actions)**
En tu repositorio GitHub:
1. **Settings** → **Secrets and variables** → **Actions**
2. **Añadir secrets**:

```
AWS_ACCESS_KEY_ID: [Tu Access Key ID]
AWS_SECRET_ACCESS_KEY: [Tu Secret Access Key]
AWS_REGION: us-east-1
STREAMLIT_SECRETS: [Token de Streamlit]
SLACK_WEBHOOK: [URL webhook Slack - opcional]
```

---

## ☁️ **PASO 3: Deploy AWS Infrastructure**

### **3.1 Inicializar Terraform**
```bash
cd infra/terraform/
terraform init
```

### **3.2 Planificar Deploy**
```bash
terraform plan

# Verificar que muestra:
# - 15-20 recursos a crear
# - 0 recursos a modificar/destruir
# - Estimación de costo: $0.00
```

### **3.3 Aplicar Configuración**
```bash
terraform apply

# Escribir: yes
# Tiempo estimado: 5-10 minutos
```

### **3.4 Verificar Recursos Creados**
```bash
# S3 Buckets
aws s3 ls | grep customer-satisfaction

# Glue Database
aws glue get-databases

# Athena Workgroup
aws athena list-work-groups

# Budget
aws budgets describe-budgets --account-id $(aws sts get-caller-identity --query Account --output text)
```

---

## 📊 **PASO 4: Configurar Servicios Externos**

### **4.1 Setup Automático**
```bash
cd ../../
python scripts/setup_external_services.py

# Este script te guiará a:
# - Configurar Streamlit Cloud
# - Conectar Google Colab
# - Setup GitHub Actions
# - Configurar notificaciones
```

### **4.2 Streamlit Cloud (Manual)**
1. **Ir a**: https://streamlit.io/cloud
2. **Connect GitHub** → Autorizar
3. **New app** → Seleccionar repo
4. **Settings**:
   - **Main file path**: `analytics/streamlit_dashboard/app.py`
   - **Python version**: 3.9
   - **Requirements**: `requirements.txt`

### **4.3 Google Colab Setup**
1. **Ir a**: https://colab.research.google.com/
2. **File** → **Open notebook** → **GitHub**
3. **Connect** → Autorizar repo
4. **Crear notebook**: `notebooks/ml_analysis.ipynb`

---

## 🤖 **PASO 5: Configurar CI/CD**

### **5.1 Activar GitHub Actions**
Los workflows ya están configurados en `.github/workflows/`:
- `data-pipeline.yml`: Pipeline principal
- `cost-monitor.yml`: Monitoreo de costos
- `terraform-plan.yml`: Validación de infrastructure

### **5.2 Configurar Triggers**
```yaml
# En .github/workflows/data-pipeline.yml
on:
  push:
    branches: [ main, dev ]
  schedule:
    - cron: '0 6 * * *'  # Ejecutar diariamente a las 6 AM
  workflow_dispatch:     # Ejecutar manualmente
```

### **5.3 Primer Deploy**
```bash
git add .
git commit -m "Initial deployment configuration"
git push origin main

# GitHub Actions se ejecutará automáticamente
```

---

## � **PASO 6: Generar y Procesar Datos**

### **6.1 Generar Datos de Prueba**
```bash
python ingestion/scripts/data_simulator.py

# Genera:
# - 1000 registros de customer feedback
# - Datos sintéticos realistas
# - Formatos CSV y JSON
```

### **6.2 Subir Datos a S3**
```bash
python ingestion/scripts/s3_uploader.py

# Sube automáticamente a:
# - s3://customer-satisfaction-raw/
# - Estructura: año/mes/día/
```

### **6.3 Ejecutar ETL Glue**
```bash
# Manual (primera vez)
aws glue start-job-run --job-name customer-satisfaction-etl

# O esperar que GitHub Actions lo ejecute automáticamente
```

---

## 🚀 **PASO 7: Verificar Funcionamiento**

### **7.1 Dashboard Streamlit**
```bash
# Local (desarrollo)
cd analytics/streamlit_dashboard/
streamlit run app.py

# Ver en: http://localhost:8501
```

### **7.2 Consultas Athena**
```sql
-- Probar en AWS Console → Athena
SELECT 
    customer_id,
    satisfaction_score,
    feedback_date
FROM customer_satisfaction_db.processed_feedback
LIMIT 10;
```

### **7.3 Verificar Costos**
```bash
python scripts/aws_cost_monitor.py

# Debe mostrar: $0.00 o muy cerca
```

---

## 🐳 **PASO 8: Docker (Alternativo)**

### **8.1 Build y Run**
```bash
cd docker/
docker-compose up -d

# Servicios disponibles:
# - Dashboard: http://localhost:8501
# - Monitoring: http://localhost:3000
# - Cost Monitor: logs en terminal
```

### **8.2 Verificar Containers**
```bash
docker-compose ps
docker-compose logs -f streamlit-dashboard
```

---

## 📊 **PASO 9: Monitoreo y Mantenimiento**

### **9.1 Monitoreo Diario**
```bash
# Script automático (ya en cron)
python scripts/aws_cost_monitor.py

# Debe enviar reporte a Slack/email
```

### **9.2 Backup y Cleanup**
```bash
# Backup semanal
python scripts/backup_data.py

# Cleanup (cuando no uses el proyecto)
terraform destroy
```

---

## ⚠️ **Troubleshooting**

### **🚨 Error: Costos Inesperados**
```bash
# ACCIÓN INMEDIATA
terraform destroy

# Investigar
aws ce get-cost-and-usage \
    --time-period Start=2025-07-01,End=2025-07-31 \
    --granularity MONTHLY \
    --metrics BlendedCost
```

### **🔧 Error: Glue Job Falla**
```bash
# Ver logs
aws logs describe-log-groups --log-group-name-prefix /aws-glue

# Re-ejecutar
aws glue start-job-run --job-name customer-satisfaction-etl
```

### **� Error: Dashboard No Carga**
```bash
# Verificar S3
aws s3 ls s3://customer-satisfaction-processed/

# Verificar Athena
aws athena get-query-execution --query-execution-id [ID]
```

### **💸 Error: Supera Free Tier**
**Límites a vigilar:**
- S3: 5GB total
- Athena: 5GB escaneado/mes
- Glue: 1M DPU-hours/mes
- CloudWatch: 5GB logs/mes

**Solución**: Usar lifecycle policies y optimizar queries.

---

## 🎯 **Checklist Final**

### **✅ Verificaciones Post-Deploy**

- [ ] **AWS Resources**: S3, Glue, Athena creados
- [ ] **Costos**: Budget configurado y funcionando
- [ ] **Dashboard**: Streamlit accesible y funcionando
- [ ] **Datos**: ETL procesando correctamente
- [ ] **Alertas**: Notificaciones llegando a Slack/email
- [ ] **GitHub Actions**: Workflows ejecutándose sin errores
- [ ] **Monitoreo**: Cost monitor reportando $0.00

### **🔄 Flujo Normal de Trabajo**

1. **Desarrollo**: Cambios en código local
2. **Testing**: `docker-compose up` para probar localmente
3. **Deploy**: `git push` → GitHub Actions se ejecuta automáticamente
4. **Monitoreo**: Verificar alertas y costos diariamente
5. **Cleanup**: `terraform destroy` cuando no uses el proyecto

---

## 📞 **Soporte**

### **🆘 En caso de problemas:**
1. **Revisar logs**: `docker-compose logs`
2. **Consultar troubleshooting** arriba
3. **GitHub Issues**: Para bugs del código
4. **AWS Support**: Para problemas de infraestructura

### **📧 Contacto del Equipo**
- **DevOps**: [email]
- **Data Engineering**: [email]
- **Slack**: #customer-analytics

---

<div align="center">

## 🎉 **¡Proyecto Desplegado Exitosamente!**

**Costo: $0.00/mes | Funcionalidad: 100% | Monitoreo: 24/7**

</div>

---

## 🎯 **ARQUITECTURA FINAL**

```
🌐 SERVICIOS EXTERNOS (GRATIS)           ☁️ AWS FREE TIER
├─ 📊 Streamlit Dashboard ($0)            ├─ 📦 S3 (5GB gratis)
├─ 📈 Grafana Cloud ($0)                 ├─ 🔍 Athena (5GB gratis)  
├─ 🤖 GitHub Actions ($0)                ├─ 🔧 Glue (1M hrs gratis)
├─ 🧠 Google Colab ($0)                  ├─ 📊 CloudWatch (5GB gratis)
├─ 🔔 Slack/Discord ($0)                 └─ 🛡️ IAM (gratis)
└─ 💾 Google Drive Backup ($0)
```

**💰 COSTO TOTAL: $0.00/mes**

---

## 🔧 **COMANDOS ÚTILES**

### **Verificar estado:**
```bash
# AWS Resources
aws s3 ls | grep customer-satisfaction
aws athena list-work-groups --query "WorkGroups[?contains(Name, 'customer')]"
aws glue get-databases --query "DatabaseList[?contains(Name, 'customer')]"

# Costos
python scripts/aws_cost_monitor.py --detailed

# Docker services
docker-compose ps
docker-compose logs streamlit-dashboard
```

### **Troubleshooting:**
```bash
# Logs detallados
terraform plan -detailed-exitcode
docker-compose logs --tail=50 -f
aws logs describe-log-groups --log-group-name-prefix "/aws/glue"

# Verificar límites
aws service-quotas get-service-quota --service-code s3 --quota-code L-DC2B2D3D
```

---

## 📞 **SOPORTE**

### **Problemas comunes:**
1. **"Terraform apply falla"** → Verificar credenciales AWS
2. **"Streamlit no conecta"** → Verificar variables .env
3. **"Costos inesperados"** → Ejecutar `terraform destroy`

### **Recursos:**
- 📖 **Docs completas**: `docs/external_services_guide.md`
- 🐛 **Issues**: GitHub Issues
- 💬 **Chat**: Slack configurado
- 📧 **Email**: Alertas automáticas configuradas

---

## 🎉 **¡LISTO!**

Con esta configuración tienes:
- ✅ **Arquitectura completa de analytics**
- ✅ **Costo garantizado: $0.00**
- ✅ **Servicios externos profesionales**
- ✅ **Automatización completa**
- ✅ **Monitoreo y alertas**

**¡Comienza a analizar satisfacción del cliente sin costos!** 🚀
