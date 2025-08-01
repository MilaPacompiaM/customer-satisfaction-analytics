# 🚀 **GUÍA RÁPIDA: CÓMO FUNCIONAR EL PROYECTO**

## ⚡ **TL;DR - Pasos Esenciales**

### **1️⃣ CONFIGURACIÓN INICIAL (Una sola vez)**

```bash
# 1. Clonar repo
git clone https://github.com/MilaPacompiaM/customer-satisfaction-analytics.git
cd customer-satisfaction-analytics

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar AWS
aws configure
# Access Key ID: [TU_ACCESS_KEY]
# Secret Access Key: [TU_SECRET_KEY]  
# Region: us-east-1
# Output: json

# 4. Configurar variables
cd infra/terraform/
cp terraform.tfvars.example terraform.tfvars
# ⚠️ EDITAR: terraform.tfvars con tu email
```

### **2️⃣ INFORMACIÓN QUE NECESITAS CAMBIAR**

#### **📧 En terraform.tfvars (OBLIGATORIO):**
```hcl
owner_email = "TU-EMAIL@ejemplo.com"     # ⚠️ CAMBIAR
alert_email = "TU-EMAIL@ejemplo.com"     # ⚠️ CAMBIAR
project_name = "customer-satisfaction-analytics"  # Opcional cambiar
environment = "dev"                      # dev o prod
```

#### **🔑 En GitHub Secrets (Para CI/CD):**
```
AWS_ACCESS_KEY_ID: [Tu Access Key]
AWS_SECRET_ACCESS_KEY: [Tu Secret Key]
AWS_REGION: us-east-1
SLACK_WEBHOOK: [Opcional - URL webhook Slack]
```

### **3️⃣ DEPLOY AUTOMÁTICO**

```bash
# Deploy infraestructura AWS (Free Tier)
terraform init
terraform apply    # Escribir: yes

# ✅ Esto crea automáticamente:
# - 3 S3 Buckets (raw, processed, curated)
# - AWS Glue (database, jobs, crawler)
# - Amazon Athena workgroup
# - CloudWatch alarms
# - AWS Budget ($1 máximo)
# - IAM roles y políticas
```

### **4️⃣ ACTIVAR SERVICIOS EXTERNOS**

```bash
# Setup automático de servicios gratuitos
cd ../../
python scripts/setup_external_services.py

# O manual:
# 1. Streamlit Cloud: https://streamlit.io/cloud
# 2. Google Colab: https://colab.research.google.com/
# 3. GitHub Actions: Ya configurado automáticamente
```

### **5️⃣ GENERAR Y PROCESAR DATOS**

```bash
# Generar datos sintéticos
python ingestion/scripts/data_simulator.py

# Subir a S3
python ingestion/scripts/s3_uploader.py

# Ejecutar ETL (o esperar GitHub Actions)
aws glue start-job-run --job-name customer-satisfaction-etl
```

### **6️⃣ VERIFICAR FUNCIONAMIENTO**

```bash
# Dashboard local
cd analytics/streamlit_dashboard/
streamlit run app.py
# Ver: http://localhost:8501

# Verificar costos (DEBE SER $0.00)
cd ../../
python scripts/aws_cost_monitor.py

# GitHub Actions
# Ir a: https://github.com/[tu-repo]/actions
```

---

## 🎯 **FLUJOS DE TRABAJO**

### **🔄 Desarrollo Diario:**
```bash
# 1. Hacer cambios en código
# 2. Testing local
docker-compose up -d

# 3. Deploy automático
git add .
git commit -m "Mi cambio"
git push origin main
# GitHub Actions se ejecuta automáticamente
```

### **💰 Deploy & Destroy (Recomendado):**
```bash
# Crear recursos para trabajar
terraform apply

# ... trabajar en el proyecto ...

# Destruir cuando termine
terraform destroy
```

### **🔍 Monitoreo Continuo:**
```bash
# Verificar costos diariamente
python scripts/aws_cost_monitor.py

# Ver logs GitHub Actions
# https://github.com/[tu-repo]/actions

# Dashboard en vivo
# https://[tu-app].streamlit.app/
```

---

## 🚨 **TROUBLESHOOTING RÁPIDO**

### **❌ Error: Costos > $0.00**
```bash
# ACCIÓN INMEDIATA
terraform destroy
```

### **❌ Error: Glue job falla**
```bash
# Ver logs
aws logs describe-log-groups --log-group-name-prefix /aws-glue
```

### **❌ Error: Dashboard no carga**
```bash
# Verificar datos
aws s3 ls s3://customer-satisfaction-processed/
```

### **❌ Error: GitHub Actions falla**
- Verificar secrets en GitHub
- Revisar logs en Actions tab
- Verificar terraform.tfvars

---

## 📊 **GENERAR DIAGRAMAS**

### **🎨 Diagramas Automáticos (Python):**
```bash
# Instalar dependencias
pip install -r requirements-diagrams.txt

# Generar diagramas
python scripts/generate_diagrams.py

# Resultado: docs/diagrams/*.png
```

### **🖌️ Diagramas Manuales (Draw.io):**
1. **Ir a**: https://app.diagrams.net/
2. **Plantilla**: AWS Architecture
3. **Componentes**: 
   - AWS: S3, Glue, Athena, CloudWatch
   - Externos: Streamlit, GitHub, Colab, Grafana
4. **Exportar**: PNG para README

### **📝 Diagramas en Código (Mermaid):**
- Ya incluidos en README.md
- Se renderizan automáticamente en GitHub
- Editables como código

---

## ✅ **CHECKLIST FINAL**

### **Pre-Deploy:**
- [ ] AWS CLI configurado
- [ ] terraform.tfvars editado con tu email
- [ ] GitHub Secrets configurados
- [ ] Dependencias Python instaladas

### **Post-Deploy:**
- [ ] `terraform apply` exitoso
- [ ] S3 buckets creados
- [ ] Glue jobs configurados
- [ ] Budget y alarmas activas
- [ ] Dashboard Streamlit funcionando
- [ ] Cost monitor reportando $0.00

### **Funcionamiento:**
- [ ] Datos generados y procesados
- [ ] ETL ejecutándose automáticamente
- [ ] Dashboard mostrando datos
- [ ] GitHub Actions sin errores
- [ ] Alertas llegando a email/Slack

---

## 🎉 **RESULTADO ESPERADO**

### **💻 Lo que tendrás funcionando:**
- ✅ **Dashboard completo**: Streamlit con visualizaciones
- ✅ **ETL automatizado**: GitHub Actions + AWS Glue
- ✅ **ML pipeline**: Google Colab conectado
- ✅ **Monitoreo 24/7**: Costos, performance, alertas
- ✅ **CI/CD completo**: Deploy automático
- ✅ **Costo $0.00**: Garantizado con protecciones

### **⏱️ Tiempos esperados:**
- **Setup inicial**: 15-30 minutos
- **Deploy AWS**: 5-10 minutos
- **Primera ejecución ETL**: 2-5 minutos
- **Dashboard activo**: Inmediato

### **📈 Capacidades:**
- **Datos**: Hasta 5GB procesamiento/mes
- **Queries**: Hasta 5GB escaneado/mes
- **ML**: GPU gratuito en Google Colab
- **Visualización**: Dashboard ilimitado
- **CI/CD**: 2000 minutos/mes GitHub Actions

---

<div align="center">

## 🚀 **¡LISTO PARA EMPEZAR!**

**Siguiente paso**: `aws configure` y editar `terraform.tfvars`

</div>
