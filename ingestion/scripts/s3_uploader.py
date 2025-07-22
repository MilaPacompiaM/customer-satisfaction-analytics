"""
Script para ingesta de datos hacia AWS S3 con arquitectura de Data Lakehouse.

Este script:
- Sube datos simulados a S3 con estructura de lakehouse
- Organiza datos por raw/processed/curated layers
- Particiona datos por fecha para optimizar consultas
- Configura metadatos para AWS Glue Data Catalog
"""

import boto3
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
from typing import Dict, List, Optional
import argparse
import logging
from botocore.exceptions import ClientError, NoCredentialsError


class S3DataLakeUploader:
    """Clase para gestionar la ingesta de datos hacia S3 Data Lake."""
    
    def __init__(self, bucket_name: str, aws_profile: Optional[str] = None):
        """
        Inicializar el uploader.
        
        Args:
            bucket_name: Nombre del bucket S3
            aws_profile: Perfil AWS a usar (opcional)
        """
        self.bucket_name = bucket_name
        self.aws_profile = aws_profile
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Inicializar cliente S3
        self._init_aws_clients()
        
        # Estructura del Data Lake
        self.lake_structure = {
            'raw': 'raw-data',
            'processed': 'processed-data', 
            'curated': 'curated-data',
            'metadata': 'metadata'
        }
        
    def _init_aws_clients(self):
        """Inicializar clientes AWS."""
        try:
            # Configurar sesión
            if self.aws_profile:
                session = boto3.Session(profile_name=self.aws_profile)
                self.s3_client = session.client('s3')
                self.glue_client = session.client('glue')
            else:
                self.s3_client = boto3.client('s3')
                self.glue_client = boto3.client('glue')
                
            # Verificar conexión
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            self.logger.info(f"Conectado exitosamente al bucket: {self.bucket_name}")
            
        except NoCredentialsError:
            self.logger.error("Credenciales AWS no encontradas")
            raise
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                self.logger.error(f"Bucket {self.bucket_name} no encontrado")
            else:
                self.logger.error(f"Error conectando a AWS: {e}")
            raise
    
    def create_partitioned_path(self, dataset_name: str, layer: str, 
                              date_col: Optional[datetime] = None) -> str:
        """
        Crear ruta particionada para S3.
        
        Args:
            dataset_name: Nombre del dataset
            layer: Capa del data lake (raw, processed, curated)
            date_col: Fecha para particionamiento
            
        Returns:
            Ruta S3 con particiones
        """
        base_path = f"{self.lake_structure[layer]}/{dataset_name}"
        
        if date_col:
            year = date_col.year
            month = f"{date_col.month:02d}"
            day = f"{date_col.day:02d}"
            return f"{base_path}/year={year}/month={month}/day={day}/"
        else:
            # Usar fecha actual si no se especifica
            today = datetime.now()
            return f"{base_path}/year={today.year}/month={today.month:02d}/day={today.day:02d}/"
    
    def upload_dataframe_as_parquet(self, df: pd.DataFrame, s3_path: str, 
                                   partition_cols: Optional[List[str]] = None) -> bool:
        """
        Subir DataFrame como archivo Parquet a S3.
        
        Args:
            df: DataFrame a subir
            s3_path: Ruta en S3
            partition_cols: Columnas para particionar
            
        Returns:
            True si se subió exitosamente
        """
        try:
            # Preparar datos para Parquet
            table = pa.Table.from_pandas(df)
            
            # Crear buffer en memoria
            import io
            buffer = io.BytesIO()
            
            if partition_cols:
                # Escribir con particiones
                pq.write_table(table, buffer, partition_cols=partition_cols)
            else:
                # Escribir archivo único
                pq.write_table(table, buffer)
            
            # Subir a S3
            buffer.seek(0)
            full_path = f"{s3_path}data.parquet"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=full_path,
                Body=buffer.getvalue(),
                ContentType='application/octet-stream'
            )
            
            self.logger.info(f"Subido exitosamente: s3://{self.bucket_name}/{full_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error subiendo {s3_path}: {e}")
            return False
    
    def upload_json_metadata(self, metadata: Dict, s3_path: str) -> bool:
        """
        Subir metadata en formato JSON.
        
        Args:
            metadata: Diccionario con metadata
            s3_path: Ruta en S3
            
        Returns:
            True si se subió exitosamente
        """
        try:
            json_data = json.dumps(metadata, indent=2, ensure_ascii=False, default=str)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_path,
                Body=json_data,
                ContentType='application/json'
            )
            
            self.logger.info(f"Metadata subida: s3://{self.bucket_name}/{s3_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error subiendo metadata {s3_path}: {e}")
            return False
    
    def process_and_upload_dataset(self, file_path: str, dataset_name: str, 
                                 layer: str = 'raw') -> bool:
        """
        Procesar y subir un dataset individual.
        
        Args:
            file_path: Ruta local del archivo
            dataset_name: Nombre del dataset
            layer: Capa del data lake
            
        Returns:
            True si se procesó exitosamente
        """
        try:
            # Leer dataset según formato
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.parquet'):
                df = pd.read_parquet(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                self.logger.error(f"Formato no soportado: {file_path}")
                return False
            
            self.logger.info(f"Procesando {dataset_name}: {len(df)} registros")
            
            # Optimizaciones de datos
            df = self._optimize_dataframe(df)
            
            # Crear ruta S3 particionada
            s3_path = self.create_partitioned_path(dataset_name, layer)
            
            # Subir DataFrame
            success = self.upload_dataframe_as_parquet(df, s3_path)
            
            if success:
                # Crear y subir metadata
                metadata = self._create_dataset_metadata(df, dataset_name, s3_path)
                metadata_path = f"{self.lake_structure['metadata']}/{dataset_name}_metadata.json"
                self.upload_json_metadata(metadata, metadata_path)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error procesando {dataset_name}: {e}")
            return False
    
    def _optimize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimizar DataFrame para almacenamiento.
        
        Args:
            df: DataFrame original
            
        Returns:
            DataFrame optimizado
        """
        # Convertir strings a categorías para reducir memoria
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:  # Si menos del 50% son únicos
                df[col] = df[col].astype('category')
        
        # Optimizar tipos de datos numéricos
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
            
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        # Convertir fechas
        date_columns = [col for col in df.columns if 'fecha' in col.lower() or 'date' in col.lower()]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        return df
    
    def _create_dataset_metadata(self, df: pd.DataFrame, dataset_name: str, s3_path: str) -> Dict:
        """
        Crear metadata del dataset.
        
        Args:
            df: DataFrame del dataset
            dataset_name: Nombre del dataset
            s3_path: Ruta en S3
            
        Returns:
            Diccionario con metadata
        """
        metadata = {
            'dataset_name': dataset_name,
            'upload_timestamp': datetime.now().isoformat(),
            's3_path': f"s3://{self.bucket_name}/{s3_path}",
            'records_count': len(df),
            'columns_count': len(df.columns),
            'size_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            'columns': {
                col: {
                    'dtype': str(df[col].dtype),
                    'null_count': int(df[col].isnull().sum()),
                    'unique_count': int(df[col].nunique())
                } for col in df.columns
            },
            'date_range': {
                'min_date': None,
                'max_date': None
            }
        }
        
        # Agregar rango de fechas si existe columna de fecha
        date_cols = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']
        if date_cols:
            main_date_col = date_cols[0]
            metadata['date_range'] = {
                'min_date': df[main_date_col].min().isoformat(),
                'max_date': df[main_date_col].max().isoformat()
            }
        
        return metadata
    
    def upload_simulated_data(self, data_dir: str = "data/simulated") -> bool:
        """
        Subir todos los datos simulados al data lake.
        
        Args:
            data_dir: Directorio con datos simulados
            
        Returns:
            True si se subieron todos exitosamente
        """
        datasets = [
            'customer_tickets',
            'nps_surveys', 
            'customer_reviews',
            'conversation_transcripts'
        ]
        
        success_count = 0
        
        for dataset in datasets:
            # Buscar archivo Parquet (preferido) o CSV
            parquet_file = os.path.join(data_dir, f"{dataset}.parquet")
            csv_file = os.path.join(data_dir, f"{dataset}.csv")
            
            if os.path.exists(parquet_file):
                file_path = parquet_file
            elif os.path.exists(csv_file):
                file_path = csv_file
            else:
                self.logger.warning(f"No se encontró archivo para {dataset}")
                continue
            
            if self.process_and_upload_dataset(file_path, dataset, 'raw'):
                success_count += 1
        
        self.logger.info(f"Subidos {success_count}/{len(datasets)} datasets exitosamente")
        return success_count == len(datasets)
    
    def create_glue_catalog_table(self, dataset_name: str, s3_path: str, 
                                database_name: str = 'customer_satisfaction_db') -> bool:
        """
        Crear tabla en AWS Glue Data Catalog.
        
        Args:
            dataset_name: Nombre del dataset
            s3_path: Ruta S3 del dataset
            database_name: Nombre de la base de datos en Glue
            
        Returns:
            True si se creó exitosamente
        """
        try:
            # Crear base de datos si no existe
            try:
                self.glue_client.create_database(
                    DatabaseInput={
                        'Name': database_name,
                        'Description': 'Base de datos para análisis de satisfacción del cliente'
                    }
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'AlreadyExistsException':
                    raise
            
            # Configuración básica de la tabla
            table_input = {
                'Name': dataset_name,
                'StorageDescriptor': {
                    'Columns': [],  # Se llenarán automáticamente por Glue Crawler
                    'Location': f"s3://{self.bucket_name}/{s3_path}",
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
                    }
                },
                'PartitionKeys': [
                    {'Name': 'year', 'Type': 'string'},
                    {'Name': 'month', 'Type': 'string'},
                    {'Name': 'day', 'Type': 'string'}
                ]
            }
            
            self.glue_client.create_table(
                DatabaseName=database_name,
                TableInput=table_input
            )
            
            self.logger.info(f"Tabla {dataset_name} creada en Glue Catalog")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando tabla Glue para {dataset_name}: {e}")
            return False
    
    def setup_data_lake_structure(self) -> bool:
        """
        Configurar estructura inicial del data lake.
        
        Returns:
            True si se configuró exitosamente
        """
        try:
            # Crear estructura de carpetas en S3
            for layer, prefix in self.lake_structure.items():
                # Crear objeto "carpeta" vacío
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=f"{prefix}/",
                    Body=b''
                )
            
            # Crear archivo README con documentación
            readme_content = """
# Customer Satisfaction Analytics Data Lake

## Estructura del Data Lake

### raw-data/
Datos crudos sin procesar, tal como se generaron o ingresaron.
Formato: Parquet particionado por fecha

### processed-data/
Datos limpiados y transformados, listos para análisis.
Incluye validaciones, normalización y enriquecimiento.

### curated-data/
Datos agregados y modelados para casos de uso específicos.
Incluye métricas de negocio y KPIs calculados.

### metadata/
Metadatos sobre los datasets, esquemas y linaje de datos.

## Particionamiento
Los datos están particionados por fecha (year/month/day) para optimizar consultas.

## Acceso
- AWS Athena: Para consultas SQL ad-hoc
- AWS QuickSight: Para dashboards y visualizaciones  
- AWS Glue: Para ETL y catalogación
- Amazon EMR: Para procesamiento big data
"""
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key="README.md",
                Body=readme_content,
                ContentType='text/markdown'
            )
            
            self.logger.info("Estructura del data lake configurada exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error configurando estructura: {e}")
            return False


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Subir datos simulados a AWS S3 Data Lake')
    parser.add_argument('--bucket', required=True, help='Nombre del bucket S3')
    parser.add_argument('--data-dir', default='data/simulated', help='Directorio con datos simulados')
    parser.add_argument('--aws-profile', help='Perfil AWS a usar')
    parser.add_argument('--setup-structure', action='store_true', 
                       help='Configurar estructura inicial del data lake')
    parser.add_argument('--create-glue-tables', action='store_true',
                       help='Crear tablas en AWS Glue Data Catalog')
    
    args = parser.parse_args()
    
    # Crear uploader
    uploader = S3DataLakeUploader(args.bucket, args.aws_profile)
    
    # Configurar estructura si se solicita
    if args.setup_structure:
        uploader.setup_data_lake_structure()
    
    # Subir datos
    success = uploader.upload_simulated_data(args.data_dir)
    
    # Crear tablas Glue si se solicita
    if args.create_glue_tables and success:
        datasets = ['customer_tickets', 'nps_surveys', 'customer_reviews', 'conversation_transcripts']
        for dataset in datasets:
            s3_path = uploader.create_partitioned_path(dataset, 'raw')
            uploader.create_glue_catalog_table(dataset, s3_path)
    
    if success:
        print(f"\n✅ Datos subidos exitosamente al bucket: {args.bucket}")
        print(f"📂 Estructura del data lake configurada")
        print(f"🔍 Datos disponibles para consulta en AWS Athena")
    else:
        print(f"\n❌ Error subiendo datos al bucket: {args.bucket}")
        exit(1)


if __name__ == "__main__":
    main() 