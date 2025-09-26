# 📊 Customer Satisfaction Analytics

<div align="center">

![Analytics](https://img.shields.io/badge/Analytics-Customer%20Satisfaction-blue)
![Cost](https://img.shields.io/badge/Cost-$0.00%2Fmonth-green)
![AWS](https://img.shields.io/badge/AWS-Free%20Tier-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**Sistema completo de análisis de satisfacción del cliente con costo $0.00**

</div>

---

## 📋 **Tabla de Contenido**

- [🎯 Resumen del Proyecto](#-resumen-del-proyecto)
- [🚀 Inicio Rápido](#-inicio-rápido)
- [🏗️ Infraestructura](#️-infraestructura) → [Ver detalles](docs/infrastructure/INFRAESTRUCTURA.md)
- [🌐 Despliegue](#-despliegue) → [Ver guía completa](docs/deployment/DESPLIEGUE.md)
- [💰 Análisis de Costos](#-análisis-de-costos) → [Ver detalles](docs/costs/COSTOS.md)
- [📚 Documentación Completa](#-documentación) → [Ver índice](docs/README.md)

---

## 🎯 **Resumen del Proyecto**

### **Problemática**
Necesidad de analizar la satisfacción del cliente a través de múltiples canales (chat, email, teléfono, presencial) sin incurrir en costos operativos elevados.

### **Solución**
Sistema de analytics completo utilizando **AWS Free Tier** y **herramientas open source** que garantiza:
- 📊 **Dashboard interactivo** con Streamlit
- 🤖 **Machine Learning** para análisis de sentimientos  
- � **Business Intelligence** con visualizaciones avanzadas
- 🛡️ **Seguridad enterprise** con IAM y cifrado
- 💰 **Costo $0.00** garantizado con monitoreo automático

### **Características Técnicas**
- **Backend**: AWS (S3, Athena, Glue) + Python
- **Frontend**: Streamlit Dashboard
- **Datos**: Simulados realistas + pipeline real opcional
- **ML**: Análisis de sentimientos con NLTK/spaCy
- **Visualización**: Plotly + métricas KPI
- **Seguridad**: IAM + cifrado + VPC
- **Costo**: $0.00/mes con límites automáticos

---

## 🚀 **Inicio Rápido**

### **Prerrequisitos**
- Windows 10/11
- Python 3.8+
- Git
- Cuenta AWS (opcional para infraestructura)

### **1. Clonar Repositorio**
```bash
git clone https://github.com/MilaPacompiaM/customer-satisfaction-analytics.git
cd customer-satisfaction-analytics
```

### **2. Configurar Entorno Python**
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements-streamlit.txt
```

### **3. Generar Datos Simulados** (Solo primera vez)
```bash
# Ejecutar simulador de datos
python scripts/data_simulator.py
```
> ⚠️ **Importante**: Los datos simulados son únicos para cada ejecución. Para desarrollo colaborativo, ejecutar solo una vez y compartir los archivos generados.

### **4. Ejecutar Dashboard**
```bash
# Opción 1: Script rápido (Windows) - RECOMENDADO
run_dashboard.bat

# Opción 2: Desde raíz del proyecto
streamlit run streamlit_app.py

# Opción 3: Directamente desde subdirectorio  
streamlit run analytics/streamlit_dashboard/app.py
```

### **5. Acceder al Dashboard**
- **URL Local**: http://localhost:8501
- **URL Red**: http://192.168.18.15:8501

---

## 🏗️ **Infraestructura**

El proyecto tiene dos modalidades de funcionamiento:

### **🔵 Modo Local (Desarrollo)**
- ✅ **Actualmente configurado**
- ✅ Datos simulados automáticos
- ✅ Sin dependencias AWS
- ✅ Perfecto para desarrollo y testing

### **🟡 Modo AWS (Producción)**
- 🔄 **En preparación**
- ✅ Terraform listo para deploy
- ✅ Infraestructura Free Tier confirmada
- ✅ Costo $0.00 garantizado

**→ [Ver arquitectura completa y detalles técnicos](docs/infrastructure/INFRAESTRUCTURA.md)**

---

## 🌐 **Despliegue**

### **Local (Listo)**
```bash
streamlit run streamlit_app.py
```

### **Streamlit Cloud (En evaluación)**
- Requiere fork del repositorio (verificando permisos)
- Archivo principal: `streamlit_app.py`
- Requirements: `requirements-streamlit.txt`

### **AWS (Preparado)**
- Infraestructura Terraform lista
- Free Tier configurado
- Deploy pendiente de aprobación

**→ [Ver guía completa de despliegue](docs/deployment/DESPLIEGUE.md)**

---

## � **Análisis de Costos**

### **Costo Actual: $0.00**
- ✅ Desarrollo 100% local
- ✅ Sin servicios AWS activos de este proyecto
- ✅ Datos simulados sin costo

### **Costo AWS (Proyectado): $0.00**
- ✅ S3: <100MB de 5GB gratuitos
- ✅ Athena: <10MB scan de 5GB gratuitos
- ✅ Glue: <2 horas de 1M gratuitas
- ✅ Límites automáticos configurados

**→ [Ver análisis detallado de costos](docs/costs/COSTOS.md)**

---

## 📁 **Estructura del Proyecto**

```
customer-satisfaction-analytics/
├── 📄 README.md                      # Este archivo (principal)
├── 🗂️ docs/                          # Documentación completa
│   ├── 📄 README.md                  # Índice de documentación
│   ├── architecture/                 # Diagramas y arquitectura
│   ├── costs/                        # Análisis de costos
│   ├── deployment/                   # Guías de despliegue
│   └── infrastructure/               # Documentación infraestructura
├── 🗂️ analytics/                     # Dashboard y análisis
│   ├── streamlit_dashboard/          # App Streamlit principal
│   ├── ml_models/                    # Modelos de ML
│   └── exploratory/                  # Análisis exploratorios
├── 🗂️ data/                          # Datos y muestras
│   ├── dummy/                        # Datos de prueba
│   ├── raw/                          # Datos crudos
│   ├── processed/                    # Datos procesados
│   └── simulated/                    # Datos simulados
├── 🗂️ storage/                       # Data Lakehouse
│   ├── lakehouse/                    # Arquitectura Delta Lake
│   ├── parquet_samples/              # Muestras Parquet
│   └── metadata_catalog/             # Glue Catalog
├── 🗂️ governance/                    # Seguridad y gobernanza
│   ├── security_policies/            # Políticas IAM
│   ├── anonymization/                # Scripts anonimización
│   └── lineage/                      # Lineaje de datos
├── 🗂️ infra/                         # Infraestructura como código
│   └── terraform/                    # Configuración AWS
├── 🗂️ scripts/                       # Utilidades y simuladores
└── 🔧 streamlit_app.py               # Punto de entrada principal
```

---

## �️ **Comandos Útiles**

### **Desarrollo**
```bash
# Activar entorno
.venv\Scripts\activate

# Ejecutar dashboard
streamlit run streamlit_app.py

# Generar nuevos datos
python scripts/data_simulator.py

# Ver costos AWS (si está configurado)
python scripts/aws_cost_monitor.py
```

### **Deploy AWS** (Futuro)
```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

---

## 👥 **Equipo y Colaboración**

- **Repositorio**: https://github.com/MilaPacompiaM/customer-satisfaction-analytics
- **Rama actual**: `Edgardo`
- **Owner**: MilaPacompiaM
- **Colaboradores**: Edgardo y equipo

### **Workflow de Desarrollo**
1. **Local first**: Desarrollo en entorno local
2. **Datos simulados**: Para desarrollo independiente
3. **AWS opcional**: Solo para producción
4. **Fork para deploy**: Si se requiere deployment externo

---

## 📞 **Soporte y Contacto**

- **Issues**: GitHub Issues
- **Documentación**: [Ver índice completo](docs/README.md)
- **Email alertas AWS**: paradox1100p@gmail.com

---

<div align="center">

**📊 Desarrollado con ❤️ para análisis de satisfacción del cliente**

[📚 **Ver documentación completa**](docs/README.md) | [🚀 **¡Comenzar Ahora!**](#-inicio-rápido)

**⭐ ¡Dale una estrella si este proyecto te es útil!**

![GitHub stars](https://img.shields.io/github/stars/MilaPacompiaM/customer-satisfaction-analytics?style=social)

</div>
