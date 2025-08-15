#!/usr/bin/env python3
"""
🚀 CONFIGURADOR AUTOMÁTICO DE SERVICIOS EXTERNOS
Análisis de Satisfacción al Cliente - Customer Satisfaction Analytics

Este script te guía paso a paso para configurar todos los servicios externos necesarios.
"""

import os
import json
import subprocess
import sys
import webbrowser
from pathlib import Path
import requests
from typing import Dict, List, Optional
from datetime import datetime

class ExternalServicesSetup:
    """Setup automático para servicios externos gratuitos."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config = {
            "proyecto": "customer-satisfaction-analytics",
            "ambiente": "production", 
            "aws_region": "us-east-1",
            "servicios_completados": []
        }
        self.errors = []
        
    def check_prerequisites(self) -> bool:
        """Verificar prerrequisitos del sistema."""
        print("🔍 Verificando prerrequisitos...")
        
        required_tools = {
            'terraform': 'terraform --version',
            'aws': 'aws --version',
            'python': 'python --version',
            'git': 'git --version'
        }
        
        for tool, command in required_tools.items():
            try:
                result = subprocess.run(command.split(), capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {tool}: OK")
                else:
                    self.errors.append(f"❌ {tool}: No encontrado")
            except FileNotFoundError:
                self.errors.append(f"❌ {tool}: No instalado")
        
        return len(self.errors) == 0
    
    def setup_terraform_config(self) -> bool:
        """Configurar Terraform con valores seguros."""
        print("\n🏗️ Configurando Terraform...")
        
        tfvars_example = self.project_root / "infra" / "terraform" / "terraform.tfvars.example"
        tfvars_file = self.project_root / "infra" / "terraform" / "terraform.tfvars"
        
        if not tfvars_file.exists():
            if tfvars_example.exists():
                import shutil
                shutil.copy(tfvars_example, tfvars_file)
                print(f"✅ Creado terraform.tfvars desde template")
            else:
                self.errors.append("❌ No se encontró terraform.tfvars.example")
                return False
        
        # Validar configuración
        with open(tfvars_file, 'r') as f:
            content = f.read()
            
        # Verificar configuraciones críticas para costo $0
        critical_configs = [
            'external_dashboard_provider = "streamlit"',
            'external_data_processor = "local"',
            'external_ml_platform = "local"'
        ]
        
        for config in critical_configs:
            if config not in content:
                print(f"⚠️ Agregando configuración crítica: {config}")
                content += f"\n{config}\n"
        
        with open(tfvars_file, 'w') as f:
            f.write(content)
            
        return True
    
    def validate_aws_credentials(self) -> bool:
        """Validar credenciales AWS."""
        print("\n🔐 Validando credenciales AWS...")
        
        try:
            result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                identity = json.loads(result.stdout)
                print(f"✅ AWS configurado para cuenta: {identity['Account']}")
                return True
            else:
                self.errors.append("❌ Credenciales AWS no configuradas")
                print("💡 Ejecuta: aws configure")
                return False
        except Exception as e:
            self.errors.append(f"❌ Error validando AWS: {e}")
            return False
    
    def setup_streamlit_config(self) -> bool:
        """Configurar Streamlit dashboard."""
        print("\n📊 Configurando Streamlit...")
        
        streamlit_dir = self.project_root / "analytics" / "streamlit_dashboard"
        env_file = streamlit_dir / ".env"
        
        if not env_file.exists():
            env_template = """# Customer Satisfaction Analytics - Streamlit Config
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DEFAULT_REGION=us-east-1

# S3 Configuration (se llena automáticamente después de terraform apply)
S3_DATA_BUCKET=
S3_RESULTS_BUCKET=

# Athena Configuration
ATHENA_WORKGROUP=
ATHENA_DATABASE=customer_satisfaction_db

# Streamlit Configuration
STREAMLIT_HOST=localhost
STREAMLIT_PORT=8501
STREAMLIT_AUTH_TOKEN=
"""
            with open(env_file, 'w') as f:
                f.write(env_template)
            print(f"✅ Creado archivo .env para Streamlit")
        
        # Verificar dependencias
        requirements_file = streamlit_dir / "requirements.txt"
        if requirements_file.exists():
            print("📦 Instalando dependencias de Streamlit...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Dependencias instaladas")
            else:
                print(f"⚠️ Error instalando dependencias: {result.stderr}")
        
        return True
    
    def setup_github_actions(self) -> bool:
        """Configurar GitHub Actions."""
        print("\n🤖 Configurando GitHub Actions...")
        
        workflows_dir = self.project_root / ".github" / "workflows"
        if not workflows_dir.exists():
            workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Verificar que el workflow existe
        workflow_file = workflows_dir / "data-pipeline.yml"
        if workflow_file.exists():
            print("✅ Workflow de GitHub Actions configurado")
            
            # Instrucciones para secrets
            print("\n📋 IMPORTANTE - Configurar GitHub Secrets:")
            print("   1. Ve a tu repositorio en GitHub")
            print("   2. Settings → Secrets and variables → Actions")
            print("   3. Agrega estos secrets:")
            print("      - AWS_ACCESS_KEY_ID")
            print("      - AWS_SECRET_ACCESS_KEY")
            print("      - SLACK_WEBHOOK_URL (opcional)")
            print("      - DISCORD_WEBHOOK_URL (opcional)")
            
        return True
    
    def setup_external_integrations(self) -> Dict:
        """Configurar integraciones externas."""
        print("\n🔗 Configurando integraciones externas...")
        
        integrations = {
            "streamlit": {
                "status": "configured",
                "url": "http://localhost:8501",
                "cost": "$0.00"
            },
            "github_actions": {
                "status": "configured", 
                "free_minutes": "2000/month",
                "cost": "$0.00"
            },
            "grafana_cloud": {
                "status": "available",
                "free_tier": "10K series, 14 days retention",
                "url": "https://grafana.com/signup",
                "cost": "$0.00"
            },
            "google_colab": {
                "status": "available",
                "free_tier": "GPU/TPU access",
                "url": "https://colab.research.google.com",
                "cost": "$0.00"
            }
        }
        
        for service, config in integrations.items():
            print(f"   📌 {service}: {config['status']} - {config['cost']}")
            
        return integrations
    
    def validate_cost_protection(self) -> bool:
        """Validar que las protecciones de costo están activas."""
        print("\n💰 Validando protecciones de costo...")
        
        terraform_dir = self.project_root / "infra" / "terraform"
        main_tf = terraform_dir / "main.tf"
        
        if not main_tf.exists():
            self.errors.append("❌ main.tf no encontrado")
            return False
        
        with open(main_tf, 'r') as f:
            content = f.read()
        
        # Verificar protecciones críticas
        protections = [
            "aws_budgets_budget",
            "zero_spend_protection", 
            "bytes_scanned_cutoff_per_query",
            "s3_storage_alarm"
        ]
        
        for protection in protections:
            if protection in content:
                print(f"   ✅ {protection}: Configurado")
            else:
                print(f"   ⚠️ {protection}: No encontrado")
        
        return True
    
    def generate_deployment_commands(self) -> List[str]:
        """Generar comandos de deployment."""
        commands = [
            "# 🚀 COMANDOS DE DEPLOYMENT",
            "",
            "# 1. Inicializar Terraform",
            "cd infra/terraform/",
            "terraform init",
            "",
            "# 2. Validar configuración",
            "terraform validate",
            "terraform plan",
            "",
            "# 3. Aplicar infraestructura (FREE TIER)",
            "terraform apply",
            "",
            "# 4. Obtener configuración para servicios externos",
            "terraform output external_integration_config",
            "",
            "# 5. Iniciar Streamlit dashboard",
            "cd ../../analytics/streamlit_dashboard/",
            "streamlit run app.py",
            "",
            "# 6. Verificar costos (debe ser $0.00)",
            "python ../../scripts/aws_cost_monitor.py",
            "",
            "# 7. IMPORTANTE: Destruir cuando no uses",
            "cd ../../infra/terraform/",
            "terraform destroy"
        ]
        return commands
    
    def run_setup(self):
        """Ejecutar setup completo."""
        print("🚀 CUSTOMER SATISFACTION ANALYTICS - SETUP AUTOMÁTICO")
        print("=" * 60)
        print("🎯 Objetivo: Configuración con costo $0.00")
        print("")
        
        steps = [
            ("Prerrequisitos", self.check_prerequisites),
            ("Configuración Terraform", self.setup_terraform_config),
            ("Credenciales AWS", self.validate_aws_credentials),
            ("Streamlit Dashboard", self.setup_streamlit_config),
            ("GitHub Actions", self.setup_github_actions),
            ("Protecciones de Costo", self.validate_cost_protection)
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            try:
                if step_func():
                    success_count += 1
                else:
                    print(f"❌ Error en: {step_name}")
            except Exception as e:
                print(f"❌ Excepción en {step_name}: {e}")
                self.errors.append(f"Error en {step_name}: {e}")
        
        # Configurar integraciones externas
        integrations = self.setup_external_integrations()
        
        # Generar comandos de deployment
        commands = self.generate_deployment_commands()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📋 RESUMEN DEL SETUP")
        print("=" * 60)
        print(f"✅ Pasos completados: {success_count}/{len(steps)}")
        print(f"❌ Errores: {len(self.errors)}")
        
        if self.errors:
            print("\n🚨 ERRORES ENCONTRADOS:")
            for error in self.errors:
                print(f"   {error}")
        
        print(f"\n💰 COSTO ESTIMADO MENSUAL: $0.00")
        print(f"🎯 SERVICIOS EXTERNOS GRATUITOS: {len(integrations)}")
        
        print("\n📋 PRÓXIMOS PASOS:")
        for cmd in commands:
            print(cmd)
        
        # Guardar configuración
        config_file = self.project_root / "setup_config.json"
        with open(config_file, 'w') as f:
            json.dump({
                "setup_date": str(subprocess.run(['date'], capture_output=True, text=True).stdout.strip()),
                "success_count": success_count,
                "total_steps": len(steps),
                "errors": self.errors,
                "integrations": integrations,
                "deployment_commands": commands
            }, f, indent=2)
        
        print(f"\n📄 Configuración guardada en: {config_file}")
        
        return len(self.errors) == 0

def main():
    """Función principal."""
    setup = ExternalServicesSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🎉 SETUP COMPLETADO EXITOSAMENTE!")
        print("💡 Ejecuta los comandos de deployment para comenzar.")
        sys.exit(0)
    else:
        print("\n❌ SETUP COMPLETADO CON ERRORES")
        print("💡 Revisa los errores y vuelve a ejecutar.")
        sys.exit(1)

if __name__ == "__main__":
    main()
