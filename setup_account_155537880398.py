#!/usr/bin/env python3
"""
🚀 CONFIGURACIÓN AUTOMÁTICA PARA CUENTA 155537880398
Script para configurar automáticamente todos los servicios para deployment inmediato
"""

import boto3
import os
import json
import subprocess
import sys
from datetime import datetime

# Configuración específica de la cuenta
AWS_ACCOUNT_ID = "155537880398"
AWS_REGION = "us-east-1"
IAM_USER = "dade01esolis"

def check_aws_config():
    """Verificar configuración AWS"""
    print("🔍 Verificando configuración AWS...")
    
    try:
        # Verificar credenciales
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print(f"✅ Cuenta AWS: {identity['Account']}")
        print(f"✅ Usuario: {identity['Arn']}")
        print(f"✅ Región: {AWS_REGION}")
        
        if identity['Account'] != AWS_ACCOUNT_ID:
            print(f"❌ ERROR: Cuenta incorrecta. Esperada: {AWS_ACCOUNT_ID}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error verificando AWS config: {e}")
        return False

def check_terraform_setup():
    """Verificar que Terraform está configurado"""
    print("\n🔧 Verificando Terraform...")
    
    try:
        # Verificar que terraform está instalado
        result = subprocess.run(['terraform', '--version'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Terraform no está instalado")
            return False
            
        print(f"✅ Terraform version: {result.stdout.split()[1]}")
        
        # Verificar que terraform.tfvars existe
        tfvars_path = "infra/terraform/terraform.tfvars"
        if not os.path.exists(tfvars_path):
            print(f"❌ Archivo {tfvars_path} no existe")
            return False
            
        print(f"✅ Archivo terraform.tfvars encontrado")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando Terraform: {e}")
        return False

def validate_s3_bucket_names():
    """Validar que los nombres de buckets están disponibles"""
    print("\n📦 Validando nombres de buckets S3...")
    
    buckets = [
        f"customer-satisfaction-data-lake-{AWS_ACCOUNT_ID}-dev",
        f"customer-satisfaction-athena-results-{AWS_ACCOUNT_ID}-dev",
        f"customer-satisfaction-logs-{AWS_ACCOUNT_ID}-dev"
    ]
    
    s3 = boto3.client('s3')
    
    for bucket_name in buckets:
        try:
            # Intentar obtener info del bucket
            s3.head_bucket(Bucket=bucket_name)
            print(f"✅ Bucket existe: {bucket_name}")
        except s3.exceptions.NoSuchBucket:
            print(f"📝 Bucket disponible para crear: {bucket_name}")
        except Exception as e:
            print(f"⚠️ Error verificando bucket {bucket_name}: {e}")

def check_iam_permissions():
    """Verificar permisos IAM necesarios"""
    print("\n🔐 Verificando permisos IAM...")
    
    required_services = ['s3', 'glue', 'athena', 'cloudwatch', 'budgets']
    
    for service in required_services:
        try:
            client = boto3.client(service)
            # Test básico para cada servicio
            if service == 's3':
                client.list_buckets()
            elif service == 'glue':
                client.get_databases()
            elif service == 'athena':
                client.list_work_groups()
            elif service == 'cloudwatch':
                client.list_metrics(MaxRecords=1)
            elif service == 'budgets':
                client.describe_budgets(AccountId=AWS_ACCOUNT_ID, MaxResults=1)
                
            print(f"✅ Permisos {service.upper()}: OK")
            
        except Exception as e:
            print(f"⚠️ Permisos {service.upper()}: {str(e)[:100]}...")

def create_github_secrets_template():
    """Crear template para GitHub Secrets"""
    print("\n🔑 Creando template para GitHub Secrets...")
    
    # Obtener las credenciales actuales
    session = boto3.Session()
    credentials = session.get_credentials()
    
    secrets_template = {
        "AWS_ACCESS_KEY_ID": credentials.access_key if credentials else "YOUR_ACCESS_KEY",
        "AWS_SECRET_ACCESS_KEY": credentials.secret_key if credentials else "YOUR_SECRET_KEY",
        "AWS_REGION": AWS_REGION,
        "AWS_ACCOUNT_ID": AWS_ACCOUNT_ID,
        "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        "NOTIFICATION_EMAIL": "edgar@tudominio.com"
    }
    
    with open("github_secrets_template.json", "w") as f:
        json.dump(secrets_template, f, indent=2)
    
    print("✅ Template creado: github_secrets_template.json")
    print("📋 Configurar estos secrets en GitHub Settings > Secrets and variables > Actions")

def setup_local_environment():
    """Configurar entorno local"""
    print("\n🐍 Configurando entorno local...")
    
    try:
        # Instalar dependencias
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencias instaladas")
        
        # Crear archivo .env local
        env_content = f"""# Configuración local para cuenta {AWS_ACCOUNT_ID}
AWS_ACCOUNT_ID={AWS_ACCOUNT_ID}
AWS_REGION={AWS_REGION}
PROJECT_PREFIX=cs-analytics-{AWS_ACCOUNT_ID}
S3_DATA_LAKE_BUCKET=customer-satisfaction-data-lake-{AWS_ACCOUNT_ID}-dev
S3_ATHENA_RESULTS_BUCKET=customer-satisfaction-athena-results-{AWS_ACCOUNT_ID}-dev
S3_LOGS_BUCKET=customer-satisfaction-logs-{AWS_ACCOUNT_ID}-dev
GLUE_DATABASE=customer_satisfaction_db_{AWS_ACCOUNT_ID}
ATHENA_WORKGROUP=customer-satisfaction-wg-{AWS_ACCOUNT_ID}
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ Archivo .env creado")
        
    except Exception as e:
        print(f"❌ Error configurando entorno: {e}")

def run_cost_check():
    """Ejecutar verificación inicial de costos"""
    print("\n💰 Ejecutando verificación inicial de costos...")
    
    try:
        result = subprocess.run([sys.executable, 'scripts/aws_cost_monitor.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Verificación de costos completada")
            print(result.stdout)
        else:
            print(f"⚠️ Warning en verificación de costos: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error ejecutando cost monitor: {e}")

def print_next_steps():
    """Imprimir próximos pasos"""
    print("\n" + "="*50)
    print("🎯 CONFIGURACIÓN COMPLETADA")
    print("="*50)
    print("\n📋 PRÓXIMOS PASOS:")
    print("\n1️⃣ EDITAR terraform.tfvars:")
    print("   - Cambiar notification_email por tu email real")
    print("   - Revisar todas las configuraciones")
    
    print("\n2️⃣ DEPLOY INFRAESTRUCTURA:")
    print("   cd infra/terraform/")
    print("   terraform init")
    print("   terraform plan")
    print("   terraform apply")
    
    print("\n3️⃣ CONFIGURAR GITHUB SECRETS:")
    print("   - Usar el archivo: github_secrets_template.json")
    print("   - Configurar en GitHub: Settings > Secrets and variables > Actions")
    
    print("\n4️⃣ GENERAR DATOS DE PRUEBA:")
    print("   python ingestion/scripts/data_simulator.py")
    print("   python ingestion/scripts/s3_uploader.py")
    
    print("\n5️⃣ INICIAR DASHBOARD:")
    print("   cd analytics/streamlit_dashboard/")
    print("   streamlit run app.py")
    
    print("\n💰 VERIFICAR COSTOS:")
    print("   python scripts/aws_cost_monitor.py")
    
    print("\n🎉 ¡LISTO PARA USAR!")

def main():
    """Función principal"""
    print("🚀 CONFIGURACIÓN AUTOMÁTICA - Customer Satisfaction Analytics")
    print(f"📊 Cuenta AWS: {AWS_ACCOUNT_ID}")
    print(f"👤 Usuario: {IAM_USER}")
    print(f"🌍 Región: {AWS_REGION}")
    print("="*60)
    
    # Verificaciones
    if not check_aws_config():
        print("❌ Configuración AWS incorrecta. Ejecutar: aws configure")
        return False
    
    if not check_terraform_setup():
        print("❌ Terraform no configurado correctamente")
        return False
    
    # Validaciones
    validate_s3_bucket_names()
    check_iam_permissions()
    
    # Configuraciones
    create_github_secrets_template()
    setup_local_environment()
    run_cost_check()
    
    # Instrucciones finales
    print_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Configuración completada exitosamente!")
        else:
            print("\n❌ Configuración falló. Revisar errores arriba.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error en configuración: {e}")
        sys.exit(1)
