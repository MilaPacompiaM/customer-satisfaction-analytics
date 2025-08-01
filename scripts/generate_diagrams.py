#!/usr/bin/env python3
"""
🎨 GENERADOR DE DIAGRAMAS DE ARQUITECTURA
Genera diagramas automáticamente usando Python Diagrams
"""

import os
from diagrams import Diagram, Edge, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Athena, Glue, GlueDataCatalog
from diagrams.aws.management import CloudwatchAlarm, Budgets
from diagrams.aws.security import IAM
from diagrams.aws.network import VPC
from diagrams.generic.blank import Blank
from diagrams.onprem.analytics import Streamlit
from diagrams.onprem.vcs import Github
from diagrams.gcp.ml import AIHub as Colab
from diagrams.generic.os import Windows as Local
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.chat import Slack

def create_architecture_diagram():
    """Crear diagrama principal de arquitectura"""
    
    # Configurar directorio de salida
    output_dir = "docs/diagrams"
    os.makedirs(output_dir, exist_ok=True)
    
    # Configurar diagrama principal
    with Diagram(
        "Customer Satisfaction Analytics - Arquitectura $0.00",
        filename=f"{output_dir}/architecture_overview",
        show=False,
        direction="TB",
        graph_attr={
            "fontsize": "20",
            "bgcolor": "white",
            "rankdir": "TB",
            "splines": "ortho"
        }
    ):
        
        # Usuarios
        with Cluster("👥 EQUIPO DE DATOS"):
            users = [
                Blank("Data Analyst"),
                Blank("Data Engineer"), 
                Blank("ML Engineer")
            ]
        
        # Servicios Externos (Gratis)
        with Cluster("🌐 SERVICIOS EXTERNOS ($0.00)"):
            streamlit = Streamlit("Dashboard\nStreamlit Cloud")
            github = Github("CI/CD\nGitHub Actions\n2000 min/mes")
            colab = Colab("ML Platform\nGoogle Colab\nGPU Gratis")
            grafana = Grafana("Monitoring\nGrafana Cloud\n10K series")
            slack = Slack("Alertas\nSlack\n10K msgs/mes")
            
        # AWS Free Tier
        with Cluster("☁️ AWS FREE TIER"):
            
            # Storage
            with Cluster("📦 ALMACENAMIENTO"):
                s3_raw = S3("Raw Data\n~100MB")
                s3_processed = S3("Processed\n~200MB")
                s3_curated = S3("Curated\n~200MB")
            
            # Processing
            with Cluster("🔧 PROCESAMIENTO"):
                glue_catalog = GlueDataCatalog("Glue Catalog\nMetadata")
                glue_etl = Glue("Glue ETL\n10 hrs/mes")
                athena = Athena("Athena\n1GB queries/mes")
            
            # Monitoring & Security
            with Cluster("🛡️ MONITOREO Y SEGURIDAD"):
                budget = Budgets("Budget Alert\n$1.00 máximo")
                cloudwatch = CloudwatchAlarm("CloudWatch\nAlarmas 80%")
                iam = IAM("IAM Roles\nSiempre gratis")
                vpc = VPC("VPC Básica\nGratis")
        
        # Desarrollo Local
        with Cluster("💻 LOCAL"):
            docker = Docker("Docker\nDevelopment")
            local = Local("Scripts\nData Gen")
        
        # Flujo de datos principal
        local >> Edge(label="upload") >> s3_raw
        s3_raw >> Edge(label="ETL") >> glue_etl
        glue_etl >> s3_processed
        s3_processed >> glue_etl >> s3_curated
        
        # Análisis y consultas
        glue_catalog >> athena
        s3_curated >> athena
        athena >> streamlit
        
        # ML Pipeline
        s3_curated >> colab
        colab >> s3_processed
        
        # Monitoreo
        glue_etl >> cloudwatch
        athena >> cloudwatch
        cloudwatch >> budget
        budget >> slack
        
        # CI/CD
        github >> glue_etl
        github >> streamlit
        github >> local
        
        # Visualización adicional
        athena >> grafana
        cloudwatch >> grafana
        
        # Conexiones de usuarios
        users[0] >> streamlit  # Data Analyst
        users[1] >> github     # Data Engineer
        users[2] >> colab      # ML Engineer
        
        # Docker para desarrollo
        docker >> streamlit
        docker >> local

def create_data_flow_diagram():
    """Crear diagrama de flujo de datos"""
    
    output_dir = "docs/diagrams"
    
    with Diagram(
        "Flujo de Datos - Pipeline ETL",
        filename=f"{output_dir}/data_flow",
        show=False,
        direction="LR",
        graph_attr={
            "fontsize": "18",
            "bgcolor": "white"
        }
    ):
        
        # Fuentes de datos
        data_gen = Local("Data\nGenerator")
        
        # Pipeline ETL
        s3_raw = S3("S3 Raw\nJSON/CSV")
        glue_job = Glue("Glue ETL\nTransform")
        s3_processed = S3("S3 Processed\nParquet")
        
        # Análisis
        athena = Athena("Athena\nSQL Queries")
        streamlit = Streamlit("Dashboard\nStreamlit")
        
        # ML
        colab = Colab("ML Training\nGoogle Colab")
        
        # Monitoreo
        cloudwatch = CloudwatchAlarm("CloudWatch\nMonitoring")
        slack = Slack("Alertas\nSlack")
        
        # Flujo
        data_gen >> Edge(label="upload") >> s3_raw
        s3_raw >> Edge(label="extract") >> glue_job
        glue_job >> Edge(label="transform") >> s3_processed
        s3_processed >> Edge(label="query") >> athena
        athena >> Edge(label="visualize") >> streamlit
        
        # ML branch
        s3_processed >> Edge(label="train") >> colab
        
        # Monitoring
        glue_job >> cloudwatch
        cloudwatch >> slack

def create_cost_diagram():
    """Crear diagrama de distribución de costos"""
    
    output_dir = "docs/diagrams"
    
    with Diagram(
        "Distribución de Recursos Free Tier",
        filename=f"{output_dir}/cost_distribution",
        show=False,
        direction="TB",
        graph_attr={
            "fontsize": "16",
            "bgcolor": "white"
        }
    ):
        
        with Cluster("📊 USO FREE TIER (Estimado)"):
            
            with Cluster("S3 Storage: 10% (500MB / 5GB)"):
                s3_usage = S3("Raw: 100MB\nProcessed: 200MB\nCurated: 200MB")
            
            with Cluster("Athena: 20% (1GB / 5GB escaneado)"):
                athena_usage = Athena("Queries diarias\n~30MB/día")
            
            with Cluster("Glue: 1% (10h / 1000h DPU)"):
                glue_usage = Glue("ETL Jobs\n20 min/día")
            
            with Cluster("CloudWatch: 20% (1GB / 5GB logs)"):
                cw_usage = CloudwatchAlarm("Logs aplicación\n~30MB/día")

def create_security_diagram():
    """Crear diagrama de capas de seguridad"""
    
    output_dir = "docs/diagrams"
    
    with Diagram(
        "Capas de Seguridad y Protección",
        filename=f"{output_dir}/security_layers",
        show=False,
        direction="TB"
    ):
        
        with Cluster("🛡️ PROTECCIONES COSTO"):
            budget = Budgets("AWS Budget\n$1 Alert")
            alarms = CloudwatchAlarm("CloudWatch Alarms\n80% Free Tier")
        
        with Cluster("🔐 SEGURIDAD AWS"):
            iam = IAM("IAM Roles\nLeast Privilege")
            vpc = VPC("VPC Basic\nNetwork Security")
        
        with Cluster("🔒 PROTECCIÓN DATOS"):
            s3_encrypt = S3("S3 Encryption\nAES-256")
        
        # Flujo de seguridad
        iam >> vpc >> s3_encrypt
        budget >> alarms

def main():
    """Generar todos los diagramas"""
    
    print("🎨 Generando diagramas de arquitectura...")
    
    try:
        # Crear directorio si no existe
        os.makedirs("docs/diagrams", exist_ok=True)
        
        # Generar diagramas
        print("📊 Creando diagrama principal...")
        create_architecture_diagram()
        
        print("🔄 Creando diagrama de flujo...")
        create_data_flow_diagram()
        
        print("💰 Creando diagrama de costos...")
        create_cost_diagram()
        
        print("🛡️ Creando diagrama de seguridad...")
        create_security_diagram()
        
        print("✅ ¡Diagramas generados exitosamente!")
        print("📁 Ubicación: docs/diagrams/")
        print("📄 Archivos:")
        print("   - architecture_overview.png")
        print("   - data_flow.png") 
        print("   - cost_distribution.png")
        print("   - security_layers.png")
        
    except ImportError:
        print("❌ Error: Librería 'diagrams' no instalada")
        print("💡 Para instalar: pip install diagrams")
        print("📖 Documentación: https://diagrams.mingrammer.com/")
        
    except Exception as e:
        print(f"❌ Error generando diagramas: {e}")
        print("💡 Usando alternativa: Draw.io o Mermaid en README")

if __name__ == "__main__":
    main()
