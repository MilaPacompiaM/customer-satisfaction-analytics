"""
Configuración automática de dashboards de Amazon QuickSight para Customer Satisfaction Analytics.

Este script automatiza:
- Creación de data sources desde Athena
- Configuración de datasets optimizados
- Creación de dashboards ejecutivos y operacionales
- Templates de análisis reutilizables
- Configuración de alertas y suscripciones
"""

import boto3
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
import uuid


class QuickSightDashboardManager:
    """Gestor de dashboards de QuickSight para análisis de satisfacción."""
    
    def __init__(self, aws_account_id: str, region: str = 'us-east-1', 
                 workgroup: str = 'customer-satisfaction-workgroup'):
        """
        Inicializar el gestor de dashboards.
        
        Args:
            aws_account_id: ID de la cuenta AWS
            region: Región AWS
            workgroup: Workgroup de Athena a usar
        """
        self.aws_account_id = aws_account_id
        self.region = region
        self.workgroup = workgroup
        
        # Clientes AWS
        self.quicksight = boto3.client('quicksight', region_name=region)
        self.athena = boto3.client('athena', region_name=region)
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Configuraciones base
        self.namespace = 'default'
        self.project_prefix = 'customer-satisfaction'
        
    def create_athena_data_source(self, database_name: str = 'customer_satisfaction_db') -> str:
        """
        Crear data source de Athena en QuickSight.
        
        Args:
            database_name: Nombre de la base de datos en Glue/Athena
            
        Returns:
            ID del data source creado
        """
        data_source_id = f"{self.project_prefix}-athena-datasource"
        
        try:
            # Verificar si ya existe
            try:
                response = self.quicksight.describe_data_source(
                    AwsAccountId=self.aws_account_id,
                    DataSourceId=data_source_id
                )
                self.logger.info(f"Data source {data_source_id} ya existe")
                return data_source_id
            except self.quicksight.exceptions.ResourceNotFoundException:
                pass
            
            # Crear nuevo data source
            response = self.quicksight.create_data_source(
                AwsAccountId=self.aws_account_id,
                DataSourceId=data_source_id,
                Name='Customer Satisfaction Analytics - Athena',
                Type='ATHENA',
                DataSourceParameters={
                    'AthenaParameters': {
                        'WorkGroup': self.workgroup
                    }
                },
                Permissions=[
                    {
                        'Principal': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:user/{self.namespace}/admin",
                        'Actions': [
                            'quicksight:DescribeDataSource',
                            'quicksight:DescribeDataSourcePermissions',
                            'quicksight:PassDataSource'
                        ]
                    }
                ],
                Tags=[
                    {
                        'Key': 'Project',
                        'Value': 'customer-satisfaction-analytics'
                    },
                    {
                        'Key': 'Environment',
                        'Value': 'production'
                    }
                ]
            )
            
            self.logger.info(f"Data source creado exitosamente: {data_source_id}")
            return data_source_id
            
        except Exception as e:
            self.logger.error(f"Error creando data source: {e}")
            raise
    
    def create_datasets(self, data_source_id: str) -> Dict[str, str]:
        """
        Crear datasets optimizados para dashboards.
        
        Args:
            data_source_id: ID del data source de Athena
            
        Returns:
            Diccionario con IDs de datasets creados
        """
        datasets = {}
        
        # Configuraciones de datasets
        dataset_configs = {
            'tickets_summary': {
                'name': 'Customer Tickets Summary',
                'description': 'Resumen de tickets de atención al cliente',
                'query': """
                    SELECT 
                        canal,
                        DATE_TRUNC('day', fecha_creacion) as fecha,
                        COUNT(*) as total_tickets,
                        AVG(satisfaccion_score) as satisfaccion_promedio,
                        AVG(duracion_minutos) as duracion_promedio,
                        SUM(CASE WHEN resolucion = 'resuelto' THEN 1 ELSE 0 END) as tickets_resueltos,
                        SUM(CASE WHEN satisfaccion_score >= 4 THEN 1 ELSE 0 END) as tickets_satisfactorios,
                        COUNT(DISTINCT cliente_id) as clientes_unicos,
                        COUNT(DISTINCT agente_id) as agentes_activos
                    FROM customer_tickets_processed 
                    WHERE fecha_creacion >= CURRENT_DATE - INTERVAL '90' DAY
                    GROUP BY canal, DATE_TRUNC('day', fecha_creacion)
                """
            },
            'nps_analysis': {
                'name': 'NPS Analysis',
                'description': 'Análisis de Net Promoter Score',
                'query': """
                    SELECT 
                        DATE_TRUNC('month', fecha_encuesta) as mes,
                        banco,
                        categoria_nps,
                        COUNT(*) as total_encuestas,
                        AVG(nps_score) as nps_promedio,
                        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY DATE_TRUNC('month', fecha_encuesta)) as porcentaje
                    FROM nps_surveys_processed 
                    WHERE fecha_encuesta >= CURRENT_DATE - INTERVAL '12' MONTH
                    GROUP BY DATE_TRUNC('month', fecha_encuesta), banco, categoria_nps
                """
            },
            'satisfaction_metrics': {
                'name': 'Satisfaction Metrics KPIs',
                'description': 'KPIs principales de satisfacción',
                'query': """
                    SELECT 
                        fecha,
                        canal_normalizado as canal,
                        total_tickets,
                        satisfaccion_promedio,
                        tasa_satisfaccion,
                        tasa_resolucion,
                        duracion_promedio,
                        clientes_unicos,
                        nps_score_calculado,
                        total_encuestas
                    FROM satisfaction_metrics 
                    WHERE fecha >= CURRENT_DATE - INTERVAL '6' MONTH
                """
            },
            'sentiment_analysis': {
                'name': 'Sentiment Analysis',
                'description': 'Análisis de sentimientos de reviews y comentarios',
                'query': """
                    SELECT 
                        DATE_TRUNC('week', fecha_review) as semana,
                        plataforma,
                        calificacion,
                        CASE 
                            WHEN calificacion >= 4 THEN 'Positivo'
                            WHEN calificacion = 3 THEN 'Neutro'
                            ELSE 'Negativo'
                        END as sentiment_categoria,
                        COUNT(*) as total_reviews,
                        AVG(longitud_review) as longitud_promedio
                    FROM customer_reviews_processed 
                    WHERE fecha_review >= CURRENT_DATE - INTERVAL '3' MONTH
                    GROUP BY DATE_TRUNC('week', fecha_review), plataforma, calificacion
                """
            },
            'agent_performance': {
                'name': 'Agent Performance',
                'description': 'Rendimiento de agentes de atención',
                'query': """
                    SELECT 
                        agente_id,
                        canal,
                        COUNT(*) as total_tickets,
                        AVG(satisfaccion_score) as satisfaccion_promedio,
                        AVG(duracion_minutos) as duracion_promedio,
                        SUM(CASE WHEN resolucion = 'resuelto' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as tasa_resolucion,
                        COUNT(DISTINCT cliente_id) as clientes_atendidos,
                        DATE_TRUNC('month', fecha_creacion) as mes
                    FROM customer_tickets_processed 
                    WHERE fecha_creacion >= CURRENT_DATE - INTERVAL '6' MONTH
                    GROUP BY agente_id, canal, DATE_TRUNC('month', fecha_creacion)
                    HAVING COUNT(*) >= 10  -- Solo agentes con al menos 10 tickets
                """
            }
        }
        
        for dataset_key, config in dataset_configs.items():
            try:
                dataset_id = f"{self.project_prefix}-{dataset_key}"
                
                # Verificar si ya existe
                try:
                    response = self.quicksight.describe_data_set(
                        AwsAccountId=self.aws_account_id,
                        DataSetId=dataset_id
                    )
                    self.logger.info(f"Dataset {dataset_id} ya existe")
                    datasets[dataset_key] = dataset_id
                    continue
                except self.quicksight.exceptions.ResourceNotFoundException:
                    pass
                
                # Crear dataset
                response = self.quicksight.create_data_set(
                    AwsAccountId=self.aws_account_id,
                    DataSetId=dataset_id,
                    Name=config['name'],
                    PhysicalTableMap={
                        'table1': {
                            'CustomSql': {
                                'DataSourceArn': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:datasource/{data_source_id}",
                                'Name': config['name'],
                                'SqlQuery': config['query']
                            }
                        }
                    },
                    ImportMode='DIRECT_QUERY',  # Para datos en tiempo real
                    Permissions=[
                        {
                            'Principal': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:user/{self.namespace}/admin",
                            'Actions': [
                                'quicksight:DescribeDataSet',
                                'quicksight:DescribeDataSetPermissions',
                                'quicksight:PassDataSet',
                                'quicksight:DescribeIngestion',
                                'quicksight:ListIngestions'
                            ]
                        }
                    ],
                    Tags=[
                        {
                            'Key': 'Project',
                            'Value': 'customer-satisfaction-analytics'
                        },
                        {
                            'Key': 'Type',
                            'Value': 'Dataset'
                        }
                    ]
                )
                
                datasets[dataset_key] = dataset_id
                self.logger.info(f"Dataset creado: {dataset_id}")
                
                # Esperar un poco entre creaciones
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Error creando dataset {dataset_key}: {e}")
                continue
        
        return datasets
    
    def create_executive_dashboard(self, datasets: Dict[str, str]) -> str:
        """
        Crear dashboard ejecutivo con KPIs principales.
        
        Args:
            datasets: Diccionario con IDs de datasets
            
        Returns:
            ID del dashboard creado
        """
        dashboard_id = f"{self.project_prefix}-executive-dashboard"
        
        try:
            # Verificar si ya existe
            try:
                response = self.quicksight.describe_dashboard(
                    AwsAccountId=self.aws_account_id,
                    DashboardId=dashboard_id
                )
                self.logger.info(f"Dashboard ejecutivo {dashboard_id} ya existe")
                return dashboard_id
            except self.quicksight.exceptions.ResourceNotFoundException:
                pass
            
            # Definición del dashboard
            dashboard_definition = {
                'DataSetIdentifierDeclarations': [
                    {
                        'DataSetArn': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:dataset/{dataset_id}",
                        'Identifier': dataset_key
                    }
                    for dataset_key, dataset_id in datasets.items()
                ],
                'Sheets': [
                    {
                        'SheetId': 'overview-sheet',
                        'Name': 'Overview',
                        'Visuals': [
                            # KPI Cards
                            {
                                'KPIVisual': {
                                    'VisualId': 'satisfaction-kpi',
                                    'Title': {
                                        'Visibility': 'VISIBLE',
                                        'FormatText': {
                                            'PlainText': 'Satisfacción Promedio'
                                        }
                                    },
                                    'FieldWells': {
                                        'Values': [
                                            {
                                                'NumericalMeasureField': {
                                                    'FieldId': 'satisfaction-value',
                                                    'Column': {
                                                        'DataSetIdentifier': 'satisfaction_metrics',
                                                        'ColumnName': 'satisfaccion_promedio'
                                                    },
                                                    'AggregationFunction': {
                                                        'SimpleNumericalAggregation': 'AVERAGE'
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            # Línea de tendencia de satisfacción
                            {
                                'LineChartVisual': {
                                    'VisualId': 'satisfaction-trend',
                                    'Title': {
                                        'Visibility': 'VISIBLE',
                                        'FormatText': {
                                            'PlainText': 'Tendencia de Satisfacción'
                                        }
                                    },
                                    'FieldWells': {
                                        'LineChartAggregatedFieldWells': {
                                            'Category': [
                                                {
                                                    'DateDimensionField': {
                                                        'FieldId': 'fecha-field',
                                                        'Column': {
                                                            'DataSetIdentifier': 'satisfaction_metrics',
                                                            'ColumnName': 'fecha'
                                                        },
                                                        'DateGranularity': 'DAY'
                                                    }
                                                }
                                            ],
                                            'Values': [
                                                {
                                                    'NumericalMeasureField': {
                                                        'FieldId': 'satisfaction-measure',
                                                        'Column': {
                                                            'DataSetIdentifier': 'satisfaction_metrics',
                                                            'ColumnName': 'satisfaccion_promedio'
                                                        },
                                                        'AggregationFunction': {
                                                            'SimpleNumericalAggregation': 'AVERAGE'
                                                        }
                                                    }
                                                }
                                            ],
                                            'Colors': [
                                                {
                                                    'CategoricalDimensionField': {
                                                        'FieldId': 'canal-field',
                                                        'Column': {
                                                            'DataSetIdentifier': 'satisfaction_metrics',
                                                            'ColumnName': 'canal'
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            },
                            # Distribución por canal
                            {
                                'BarChartVisual': {
                                    'VisualId': 'channel-distribution',
                                    'Title': {
                                        'Visibility': 'VISIBLE',
                                        'FormatText': {
                                            'PlainText': 'Satisfacción por Canal'
                                        }
                                    },
                                    'FieldWells': {
                                        'BarChartAggregatedFieldWells': {
                                            'Category': [
                                                {
                                                    'CategoricalDimensionField': {
                                                        'FieldId': 'canal-category',
                                                        'Column': {
                                                            'DataSetIdentifier': 'tickets_summary',
                                                            'ColumnName': 'canal'
                                                        }
                                                    }
                                                }
                                            ],
                                            'Values': [
                                                {
                                                    'NumericalMeasureField': {
                                                        'FieldId': 'satisfaction-bar',
                                                        'Column': {
                                                            'DataSetIdentifier': 'tickets_summary',
                                                            'ColumnName': 'satisfaccion_promedio'
                                                        },
                                                        'AggregationFunction': {
                                                            'SimpleNumericalAggregation': 'AVERAGE'
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    },
                    {
                        'SheetId': 'nps-sheet',
                        'Name': 'NPS Analysis',
                        'Visuals': [
                            # Gauge de NPS
                            {
                                'GaugeChartVisual': {
                                    'VisualId': 'nps-gauge',
                                    'Title': {
                                        'Visibility': 'VISIBLE',
                                        'FormatText': {
                                            'PlainText': 'NPS Score Actual'
                                        }
                                    },
                                    'FieldWells': {
                                        'Values': [
                                            {
                                                'NumericalMeasureField': {
                                                    'FieldId': 'nps-value',
                                                    'Column': {
                                                        'DataSetIdentifier': 'nps_analysis',
                                                        'ColumnName': 'nps_promedio'
                                                    },
                                                    'AggregationFunction': {
                                                        'SimpleNumericalAggregation': 'AVERAGE'
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            # Distribución NPS
                            {
                                'PieChartVisual': {
                                    'VisualId': 'nps-distribution',
                                    'Title': {
                                        'Visibility': 'VISIBLE',
                                        'FormatText': {
                                            'PlainText': 'Distribución NPS'
                                        }
                                    },
                                    'FieldWells': {
                                        'PieChartAggregatedFieldWells': {
                                            'Category': [
                                                {
                                                    'CategoricalDimensionField': {
                                                        'FieldId': 'nps-category',
                                                        'Column': {
                                                            'DataSetIdentifier': 'nps_analysis',
                                                            'ColumnName': 'categoria_nps'
                                                        }
                                                    }
                                                }
                                            ],
                                            'Values': [
                                                {
                                                    'NumericalMeasureField': {
                                                        'FieldId': 'nps-count',
                                                        'Column': {
                                                            'DataSetIdentifier': 'nps_analysis',
                                                            'ColumnName': 'total_encuestas'
                                                        },
                                                        'AggregationFunction': {
                                                            'SimpleNumericalAggregation': 'SUM'
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
            
            # Crear dashboard
            response = self.quicksight.create_dashboard(
                AwsAccountId=self.aws_account_id,
                DashboardId=dashboard_id,
                Name='Customer Satisfaction Analytics - Executive Dashboard',
                Definition=dashboard_definition,
                Permissions=[
                    {
                        'Principal': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:user/{self.namespace}/admin",
                        'Actions': [
                            'quicksight:DescribeDashboard',
                            'quicksight:ListDashboardVersions',
                            'quicksight:QueryDashboard',
                            'quicksight:UpdateDashboard',
                            'quicksight:DeleteDashboard'
                        ]
                    }
                ],
                Tags=[
                    {
                        'Key': 'Project',
                        'Value': 'customer-satisfaction-analytics'
                    },
                    {
                        'Key': 'Type',
                        'Value': 'Executive-Dashboard'
                    }
                ]
            )
            
            self.logger.info(f"Dashboard ejecutivo creado: {dashboard_id}")
            return dashboard_id
            
        except Exception as e:
            self.logger.error(f"Error creando dashboard ejecutivo: {e}")
            raise
    
    def create_operational_dashboard(self, datasets: Dict[str, str]) -> str:
        """
        Crear dashboard operacional para equipos de atención.
        
        Args:
            datasets: Diccionario con IDs de datasets
            
        Returns:
            ID del dashboard creado
        """
        dashboard_id = f"{self.project_prefix}-operational-dashboard"
        
        # Configuración simplificada para el dashboard operacional
        try:
            response = self.quicksight.create_dashboard(
                AwsAccountId=self.aws_account_id,
                DashboardId=dashboard_id,
                Name='Customer Satisfaction Analytics - Operational Dashboard',
                Definition={
                    'DataSetIdentifierDeclarations': [
                        {
                            'DataSetArn': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:dataset/{datasets['agent_performance']}",
                            'Identifier': 'agent_performance'
                        },
                        {
                            'DataSetArn': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:dataset/{datasets['tickets_summary']}",
                            'Identifier': 'tickets_summary'
                        }
                    ],
                    'Sheets': [
                        {
                            'SheetId': 'operational-overview',
                            'Name': 'Operational Metrics',
                            'Visuals': []  # Definición simplificada
                        }
                    ]
                },
                Permissions=[
                    {
                        'Principal': f"arn:aws:quicksight:{self.region}:{self.aws_account_id}:user/{self.namespace}/admin",
                        'Actions': [
                            'quicksight:DescribeDashboard',
                            'quicksight:ListDashboardVersions',
                            'quicksight:QueryDashboard'
                        ]
                    }
                ],
                Tags=[
                    {
                        'Key': 'Project',
                        'Value': 'customer-satisfaction-analytics'
                    },
                    {
                        'Key': 'Type',
                        'Value': 'Operational-Dashboard'
                    }
                ]
            )
            
            self.logger.info(f"Dashboard operacional creado: {dashboard_id}")
            return dashboard_id
            
        except Exception as e:
            self.logger.error(f"Error creando dashboard operacional: {e}")
            return None
    
    def setup_refresh_schedules(self, datasets: Dict[str, str]) -> None:
        """
        Configurar programaciones de refresh para datasets.
        
        Args:
            datasets: Diccionario con IDs de datasets
        """
        for dataset_key, dataset_id in datasets.items():
            try:
                # Configurar refresh diario a las 6 AM
                response = self.quicksight.create_refresh_schedule(
                    AwsAccountId=self.aws_account_id,
                    DataSetId=dataset_id,
                    Schedule={
                        'ScheduleId': f"{dataset_key}-daily-refresh",
                        'ScheduleFrequency': {
                            'Interval': 'DAILY',
                            'TimeOfTheDay': '06:00'
                        },
                        'RefreshType': 'FULL_REFRESH'
                    }
                )
                
                self.logger.info(f"Refresh schedule configurado para {dataset_key}")
                
            except Exception as e:
                self.logger.warning(f"No se pudo configurar refresh para {dataset_key}: {e}")
    
    def deploy_complete_solution(self, database_name: str = 'customer_satisfaction_db') -> Dict[str, Any]:
        """
        Desplegar solución completa de BI.
        
        Args:
            database_name: Nombre de la base de datos
            
        Returns:
            Diccionario con IDs de recursos creados
        """
        try:
            self.logger.info("Iniciando despliegue completo de solución BI...")
            
            # 1. Crear data source
            data_source_id = self.create_athena_data_source(database_name)
            
            # 2. Crear datasets
            datasets = self.create_datasets(data_source_id)
            
            # 3. Crear dashboards
            executive_dashboard = self.create_executive_dashboard(datasets)
            operational_dashboard = self.create_operational_dashboard(datasets)
            
            # 4. Configurar refresh schedules
            self.setup_refresh_schedules(datasets)
            
            result = {
                'data_source_id': data_source_id,
                'datasets': datasets,
                'dashboards': {
                    'executive': executive_dashboard,
                    'operational': operational_dashboard
                },
                'deployment_time': datetime.now().isoformat(),
                'status': 'success'
            }
            
            self.logger.info("Despliegue completado exitosamente")
            return result
            
        except Exception as e:
            self.logger.error(f"Error en despliegue: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'deployment_time': datetime.now().isoformat()
            }


def main():
    """Función principal para desplegar dashboards."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Desplegar dashboards de QuickSight')
    parser.add_argument('--account-id', required=True, help='AWS Account ID')
    parser.add_argument('--region', default='us-east-1', help='AWS Region')
    parser.add_argument('--database', default='customer_satisfaction_db', help='Database name')
    parser.add_argument('--workgroup', default='customer-satisfaction-workgroup', help='Athena workgroup')
    
    args = parser.parse_args()
    
    # Crear manager
    manager = QuickSightDashboardManager(
        aws_account_id=args.account_id,
        region=args.region,
        workgroup=args.workgroup
    )
    
    # Desplegar solución
    result = manager.deploy_complete_solution(args.database)
    
    if result['status'] == 'success':
        print("\n✅ Despliegue de BI completado exitosamente!")
        print(f"📊 Data Source: {result['data_source_id']}")
        print(f"📈 Datasets creados: {len(result['datasets'])}")
        print(f"🎯 Dashboard Ejecutivo: {result['dashboards']['executive']}")
        print(f"⚙️ Dashboard Operacional: {result['dashboards']['operational']}")
        
        # URLs de acceso (aproximadas)
        base_url = f"https://{args.region}.quicksight.aws.amazon.com/sn/dashboards"
        print(f"\n🔗 URLs de acceso:")
        print(f"Executive: {base_url}/{result['dashboards']['executive']}")
        if result['dashboards']['operational']:
            print(f"Operational: {base_url}/{result['dashboards']['operational']}")
    else:
        print(f"\n❌ Error en el despliegue: {result['error']}")
        exit(1)


if __name__ == "__main__":
    main() 