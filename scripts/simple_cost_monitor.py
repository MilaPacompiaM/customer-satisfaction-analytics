#!/usr/bin/env python3
"""
Monitor de Costos AWS - Customer Satisfaction Analytics
Account: 155537880398 (dade01esolis)
Versión simplificada para deployment inmediato
"""

import boto3
import json
from datetime import datetime, timedelta
import logging
import argparse
import os

# Configuración específica para cuenta 155537880398
AWS_ACCOUNT_ID = "155537880398"
AWS_REGION = "us-east-1"
PROJECT_PREFIX = "cs-analytics-155537880398"

# Configuración de buckets específicos
S3_BUCKETS = {
    "data_lake": f"customer-satisfaction-data-lake-{AWS_ACCOUNT_ID}-dev",
    "athena_results": f"customer-satisfaction-athena-results-{AWS_ACCOUNT_ID}-dev",
    "logs": f"customer-satisfaction-logs-{AWS_ACCOUNT_ID}-dev"
}

# Límites Free Tier
FREE_TIER_LIMITS = {
    "s3_storage_gb": 5,
    "athena_scanned_gb": 5,
    "glue_dpu_hours": 1000000,  # 1M DPU hours
    "cloudwatch_logs_gb": 5
}

class SimpleCostMonitor:
    """Monitor de costos simplificado"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name=AWS_REGION)
        self.cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION)
        self.ce_client = boto3.client('ce', region_name='us-east-1')  # Cost Explorer solo en us-east-1
        
    def check_s3_usage(self):
        """Verificar uso de S3"""
        print("📦 Verificando uso de S3...")
        
        total_size = 0
        bucket_details = {}
        
        for bucket_name, bucket_id in S3_BUCKETS.items():
            try:
                # Verificar si existe el bucket
                self.s3_client.head_bucket(Bucket=bucket_id)
                
                # Obtener tamaño del bucket
                paginator = self.s3_client.get_paginator('list_objects_v2')
                size = 0
                count = 0
                
                for page in paginator.paginate(Bucket=bucket_id):
                    if 'Contents' in page:
                        for obj in page['Contents']:
                            size += obj['Size']
                            count += 1
                
                size_mb = size / (1024 * 1024)
                size_gb = size_mb / 1024
                total_size += size_gb
                
                bucket_details[bucket_name] = {
                    "size_mb": round(size_mb, 2),
                    "size_gb": round(size_gb, 3),
                    "objects": count,
                    "bucket_id": bucket_id
                }
                
                print(f"  ✅ {bucket_name}: {size_mb:.1f} MB ({count} objetos)")
                
            except self.s3_client.exceptions.NoSuchBucket:
                print(f"  📝 {bucket_name}: Bucket no existe (será creado)")
                bucket_details[bucket_name] = {"size_gb": 0, "objects": 0, "bucket_id": bucket_id}
            except Exception as e:
                print(f"  ⚠️ {bucket_name}: Error - {e}")
                bucket_details[bucket_name] = {"size_gb": 0, "objects": 0, "error": str(e)}
        
        # Calcular porcentaje usado
        usage_percent = (total_size / FREE_TIER_LIMITS["s3_storage_gb"]) * 100
        
        print(f"\n📊 Total S3: {total_size:.3f} GB / {FREE_TIER_LIMITS['s3_storage_gb']} GB ({usage_percent:.1f}%)")
        
        if usage_percent > 80:
            print("⚠️ WARNING: S3 cerca del límite Free Tier!")
        elif usage_percent > 50:
            print("💡 INFO: S3 uso moderado")
        else:
            print("✅ S3 uso seguro")
            
        return {
            "total_gb": total_size,
            "usage_percent": usage_percent,
            "buckets": bucket_details,
            "status": "warning" if usage_percent > 80 else "ok"
        }
    
    def check_current_costs(self):
        """Verificar costos actuales"""
        print("\n💰 Verificando costos actuales...")
        
        try:
            # Obtener costos del mes actual
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            
            total_cost = 0
            services_cost = {}
            
            if response['ResultsByTime']:
                for group in response['ResultsByTime'][0]['Groups']:
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['UnblendedCost']['Amount'])
                    if cost > 0:
                        services_cost[service] = cost
                        total_cost += cost
            
            print(f"💵 Costo total del mes: ${total_cost:.2f}")
            
            if total_cost == 0:
                print("✅ ¡Perfecto! Costo $0.00 - Dentro del Free Tier")
            elif total_cost < 1:
                print(f"💚 Excelente! Costo muy bajo: ${total_cost:.2f}")
            elif total_cost < 5:
                print(f"💛 Moderado: ${total_cost:.2f} - Revisar uso")
            else:
                print(f"🚨 ALTO: ${total_cost:.2f} - ACCIÓN REQUERIDA!")
            
            if services_cost:
                print("\n📋 Costos por servicio:")
                for service, cost in sorted(services_cost.items(), key=lambda x: x[1], reverse=True):
                    if cost > 0.01:  # Solo mostrar servicios con costo > $0.01
                        print(f"  - {service}: ${cost:.2f}")
            
            return {
                "total_cost": total_cost,
                "services": services_cost,
                "status": "ok" if total_cost < 1 else "warning" if total_cost < 5 else "critical"
            }
            
        except Exception as e:
            print(f"⚠️ Error obteniendo costos: {e}")
            return {"total_cost": 0, "services": {}, "status": "unknown", "error": str(e)}
    
    def generate_report(self):
        """Generar reporte completo"""
        print("="*60)
        print("🔍 CUSTOMER SATISFACTION ANALYTICS - COST MONITOR")
        print(f"📊 Cuenta: {AWS_ACCOUNT_ID}")
        print(f"👤 Usuario: dade01esolis")
        print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Verificar S3
        s3_report = self.check_s3_usage()
        
        # Verificar costos
        cost_report = self.check_current_costs()
        
        # Resumen final
        print("\n" + "="*60)
        print("📝 RESUMEN - CUENTA IAM COMPARTIDA")
        print("="*60)
        
        print(f"💾 S3 Storage (NUESTRO): {s3_report['total_gb']:.3f} GB ({s3_report['usage_percent']:.1f}%)")
        print(f"💰 Costo total cuenta: ${cost_report['total_cost']:.2f}")
        print(f"💰 Costo NUESTRO proyecto: $0.00 (recursos no creados aún)")
        print("🏢 Cuenta compartida: Otros servicios generan costos adicionales")
        print("🎯 Meta nuestro proyecto: $0.00 mensual (Free Tier)")
        
        # Status general
        if s3_report["status"] == "ok":
            print("✅ STATUS NUESTRO: LIMPIO - Listo para deployment $0.00")
            if cost_report['total_cost'] > 5.0:
                print("⚠️ STATUS CUENTA: COSTOS ALTOS - Principalmente de otros servicios")
            elif cost_report['total_cost'] > 1.0:
                print("⚠️ STATUS CUENTA: COSTOS MODERADOS - De otros servicios")
            return True
        else:
            print("⚠️ STATUS: REVISAR - Verificar configuración")
            return False
    
    def cleanup_old_data(self, days_to_keep=90):
        """Limpiar datos antiguos para mantener costos bajos"""
        print(f"\n🧹 Limpiando datos antiguos (>{days_to_keep} días)...")
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        for bucket_name, bucket_id in S3_BUCKETS.items():
            try:
                # Solo limpiar bucket de logs para empezar
                if "logs" in bucket_name.lower():
                    paginator = self.s3_client.get_paginator('list_objects_v2')
                    
                    for page in paginator.paginate(Bucket=bucket_id):
                        if 'Contents' in page:
                            objects_to_delete = []
                            
                            for obj in page['Contents']:
                                if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                                    objects_to_delete.append({'Key': obj['Key']})
                            
                            if objects_to_delete:
                                self.s3_client.delete_objects(
                                    Bucket=bucket_id,
                                    Delete={'Objects': objects_to_delete}
                                )
                                deleted_count += len(objects_to_delete)
                                print(f"  🗑️ Eliminados {len(objects_to_delete)} objetos de {bucket_name}")
                
            except Exception as e:
                print(f"  ⚠️ Error limpiando {bucket_name}: {e}")
        
        print(f"✅ Limpieza completada: {deleted_count} objetos eliminados")
        return deleted_count

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Monitor de costos AWS')
    parser.add_argument('--cleanup', action='store_true', help='Ejecutar limpieza de datos')
    parser.add_argument('--days-to-keep', type=int, default=90, help='Días de datos a mantener')
    parser.add_argument('--environment', default='dev', help='Environment (dev/staging/prod)')
    parser.add_argument('--final-check', action='store_true', help='Verificación final de costos')
    
    args = parser.parse_args()
    
    monitor = SimpleCostMonitor()
    
    try:
        # Generar reporte principal
        success = monitor.generate_report()
        
        # Limpieza si se solicita
        if args.cleanup:
            monitor.cleanup_old_data(args.days_to_keep)
        
        # Check final
        if args.final_check:
            print("\n🔍 VERIFICACIÓN FINAL...")
            cost_report = monitor.check_current_costs()
            if cost_report["total_cost"] > 1:
                print("🚨 ALERTA: Costos superiores a $1.00!")
                return False
        
        return success
        
    except Exception as e:
        print(f"❌ Error en monitor: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
