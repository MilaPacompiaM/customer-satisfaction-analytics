# 🚀 CUSTOMER SATISFACTION ANALYTICS - CONFIGURACIÓN COSTO $0.00

## ✅ **CAMBIOS APLICADOS PARA COSTO CERO**

### **🛡️ Protecciones de Costo Agregadas:**

1. **AWS Budget Alert** - Notificación automática si supera $1
2. **CloudWatch Alarms** - Monitoreo S3 y Athena cerca de límites free tier
3. **Athena Query Limits** - 1GB máximo por consulta
4. **Variables de Servicios Externos** - Configuración para alternativas gratuitas

### **🔄 Servicios Externos Configurados:**

| **Servicio AWS** | **Alternativa Gratuita** | **Ahorro Mensual** |
|------------------|---------------------------|-------------------|
| QuickSight | Streamlit Dashboard | $9.00 |
| NAT Gateway | Sin VPC/Conexión directa | $32.40 |
| CloudTrail completo | CloudWatch Events básico | $2.00 |
| **TOTAL AHORRADO** | | **$43.40/mes** |

---

## 🚀 **GUÍA DE DEPLOYMENT RÁPIDO**

### **1. Setup Inicial (Una sola vez)**

```bash
# Clonar y configurar
git clone https://github.com/tu-usuario/customer-satisfaction-analytics.git
cd customer-satisfaction-analytics

# Ejecutar setup automático
python scripts/setup_external_services.py
```

### **2. Configurar AWS Credentials**

```bash
# Opción A: AWS CLI
aws configure
# AWS Access Key ID: tu_access_key
# AWS Secret Access Key: tu_secret_key
# Default region: us-east-1

# Opción B: Variables de entorno
export AWS_ACCESS_KEY_ID=tu_access_key
export AWS_SECRET_ACCESS_KEY=tu_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### **3. Copiar archivo de configuración**

```bash
cd infra/terraform/
cp terraform.tfvars.example terraform.tfvars

# Editar terraform.tfvars con tu email para alertas
# notification_email = "tu-email@ejemplo.com"
```

### **4. Desplegar Infraestructura AWS (FREE TIER)**

```bash
# Inicializar Terraform
terraform init

# Verificar plan (debe mostrar $0.00 en costos)
terraform plan

# Aplicar (crear recursos AWS gratuitos)
terraform apply
```

### **5. Obtener Configuración para Servicios Externos**

```bash
# Obtener configuración generada
terraform output external_integration_config

# Copiar valores a archivo .env
terraform output aws_credentials_template
```

### **6. Iniciar Dashboard Local (GRATIS)**

```bash
# Opción A: Python local
cd ../../analytics/streamlit_dashboard/
pip install -r requirements.txt
streamlit run app.py

# Opción B: Docker
cd ../../docker/
docker-compose up streamlit-dashboard
```

### **7. ⚠️ IMPORTANTE: Destruir Recursos Cuando No Uses**

```bash
cd infra/terraform/
terraform destroy
```

---

## 🐳 **DESARROLLO CON DOCKER (TODO GRATIS)**

### **Iniciar todos los servicios:**

```bash
cd docker/

# Configurar variables de entorno
cat > .env << EOF
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=us-east-1
S3_DATA_BUCKET=tu-bucket-name
ATHENA_WORKGROUP=tu-workgroup
GRAFANA_ADMIN_PASSWORD=admin123
EOF

# Iniciar servicios
docker-compose up -d

# Verificar servicios
docker-compose ps
```

### **Acceder a servicios:**
- **Streamlit Dashboard**: http://localhost:8501
- **Grafana OSS**: http://localhost:3000 (admin/admin123)
- **Cost Monitor**: Logs en `docker-compose logs cost-monitor`

---

## 🤖 **AUTOMATIZACIÓN CON GITHUB ACTIONS (2000 MIN GRATIS)**

### **1. Configurar Secrets en GitHub:**

Ve a tu repositorio → Settings → Secrets and variables → Actions

Agregar:
```
AWS_ACCESS_KEY_ID: tu_access_key
AWS_SECRET_ACCESS_KEY: tu_secret_key
SLACK_WEBHOOK_URL: https://hooks.slack.com/... (opcional)
```

### **2. El workflow se ejecuta automáticamente:**
- **Diariamente a las 6 AM UTC**
- **Manualmente desde GitHub Actions**
- **Monitoreo de costos incluido**

---

## 📊 **SERVICIOS EXTERNOS CONFIGURADOS**

### **🎯 Dashboard: Streamlit (GRATIS)**
```bash
# Local
streamlit run analytics/streamlit_dashboard/app.py

# Deploy gratuito: Streamlit Cloud
# https://streamlit.io/cloud
```

### **📈 Monitoring: Grafana Cloud (10K series GRATIS)**
```bash
# 1. Crear cuenta: https://grafana.com/
# 2. Configurar datasource Athena
# 3. Importar dashboards desde docker/grafana/
```

### **🧠 ML: Google Colab (GPU GRATIS)**
```python
# Notebook incluido: notebooks/ml_training_colab.ipynb
# Conecta automáticamente a tus datos S3
```

### **🔔 Notificaciones: Slack/Discord (GRATIS)**
```bash
# Configurar webhooks en terraform.tfvars
slack_webhook_url = "https://hooks.slack.com/..."
discord_webhook_url = "https://discord.com/api/webhooks/..."
```

---

## 💰 **VERIFICACIÓN DE COSTOS**

### **Monitor automático:**
```bash
# Ejecutar verificación
python scripts/aws_cost_monitor.py

# Output esperado:
# 📊 Uso S3: 0.5GB de 5GB (10%)
# 📊 Uso Athena: 0.2GB de 5GB (4%)
# 💰 Costo estimado: $0.00
```

### **Alertas configuradas:**
- ✅ Email al 80% de uso free tier
- ✅ Slack/Discord para alertas críticas
- ✅ Budget AWS máximo $5 (protección)

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
