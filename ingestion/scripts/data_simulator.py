"""
Generador de datos sintéticos para análisis de satisfacción del cliente bancario.

Este script simula:
- Tickets de atención al cliente
- Encuestas de satisfacción (NPS)
- Reviews de clientes
- Transcripciones de conversaciones
- Métricas de interacción
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import json
import os
from typing import Dict, List, Tuple
import argparse
import logging


class CustomerSatisfactionDataSimulator:
    """Simulador de datos de satisfacción del cliente."""
    
    def __init__(self, locale='es_ES', seed=42):
        """
        Inicializar el simulador.
        
        Args:
            locale: Configuración regional para Faker
            seed: Semilla para reproducibilidad
        """
        self.fake = Faker(locale)
        Faker.seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Configuraciones del dominio bancario
        self.channels = ['telefono', 'chat', 'email', 'presencial', 'app_movil']
        self.departments = [
            'cuentas_corrientes', 'tarjetas_credito', 'prestamos',
            'inversiones', 'seguros', 'banca_digital', 'soporte_tecnico'
        ]
        self.issues = [
            'consulta_saldo', 'problema_tarjeta', 'solicitud_prestamo',
            'reclamo_cargo', 'actualizacion_datos', 'bloqueo_cuenta',
            'transferencia_internacional', 'problema_app', 'consulta_seguro'
        ]
        self.resolutions = [
            'resuelto', 'escalado', 'pendiente', 'cerrado_sin_resolucion'
        ]
        self.banks = [
            'Banco Nacional', 'Banco Popular', 'Banco Central',
            'Banco del Estado', 'Banco Internacional'
        ]
        
    def generate_customer_tickets(self, num_tickets: int = 10000) -> pd.DataFrame:
        """
        Generar tickets de atención al cliente.
        
        Args:
            num_tickets: Número de tickets a generar
            
        Returns:
            DataFrame con tickets simulados
        """
        self.logger.info(f"Generando {num_tickets} tickets de atención al cliente...")
        
        tickets = []
        start_date = datetime.now() - timedelta(days=365)
        
        for i in range(num_tickets):
            # Fecha aleatoria en el último año
            ticket_date = start_date + timedelta(
                days=random.randint(0, 365),
                hours=random.randint(8, 20),
                minutes=random.randint(0, 59)
            )
            
            # Generar datos del ticket
            channel = random.choice(self.channels)
            department = random.choice(self.departments)
            issue = random.choice(self.issues)
            
            # Duración basada en canal (distribución realista)
            if channel == 'telefono':
                duration_minutes = max(1, int(np.random.normal(12, 5)))
            elif channel == 'chat':
                duration_minutes = max(1, int(np.random.normal(8, 3)))
            elif channel == 'email':
                duration_minutes = max(5, int(np.random.normal(240, 120)))  # Email más lento
            elif channel == 'presencial':
                duration_minutes = max(2, int(np.random.normal(15, 7)))
            else:  # app_movil
                duration_minutes = max(1, int(np.random.normal(5, 2)))
            
            # Satisfacción influenciada por duración y resolución
            resolution = random.choice(self.resolutions)
            if resolution == 'resuelto':
                satisfaction_base = 4.2
            elif resolution == 'escalado':
                satisfaction_base = 3.0
            elif resolution == 'pendiente':
                satisfaction_base = 2.5
            else:
                satisfaction_base = 1.8
                
            # Ajustar por duración (más tiempo = menor satisfacción)
            if duration_minutes > 20:
                satisfaction_base -= 0.5
            elif duration_minutes > 10:
                satisfaction_base -= 0.2
                
            satisfaction = max(1, min(5, satisfaction_base + np.random.normal(0, 0.8)))
            
            ticket = {
                'ticket_id': f'TKT-{i+1:06d}',
                'fecha_creacion': ticket_date,
                'cliente_id': f'CLI-{random.randint(1000, 99999):05d}',
                'canal': channel,
                'departamento': department,
                'tipo_consulta': issue,
                'duracion_minutos': duration_minutes,
                'resolucion': resolution,
                'satisfaccion_score': round(satisfaction, 1),
                'agente_id': f'AGT-{random.randint(1, 100):03d}',
                'sucursal_id': f'SUC-{random.randint(1, 50):03d}' if channel == 'presencial' else None,
                'prioridad': random.choices(
                    ['baja', 'media', 'alta', 'critica'],
                    weights=[40, 35, 20, 5]
                )[0],
                'cliente_vip': random.choices([True, False], weights=[10, 90])[0]
            }
            
            tickets.append(ticket)
            
        df = pd.DataFrame(tickets)
        self.logger.info(f"Generados {len(df)} tickets exitosamente")
        return df
    
    def generate_nps_surveys(self, num_surveys: int = 5000) -> pd.DataFrame:
        """
        Generar encuestas NPS (Net Promoter Score).
        
        Args:
            num_surveys: Número de encuestas a generar
            
        Returns:
            DataFrame con encuestas NPS
        """
        self.logger.info(f"Generando {num_surveys} encuestas NPS...")
        
        surveys = []
        start_date = datetime.now() - timedelta(days=365)
        
        for i in range(num_surveys):
            survey_date = start_date + timedelta(
                days=random.randint(0, 365)
            )
            
            # Score NPS (0-10)
            nps_score = random.choices(
                range(0, 11),
                weights=[5, 8, 10, 12, 15, 18, 20, 15, 10, 8, 5]  # Distribución realista
            )[0]
            
            # Categoría NPS
            if nps_score >= 9:
                categoria = 'promotor'
            elif nps_score >= 7:
                categoria = 'neutro'
            else:
                categoria = 'detractor'
            
            # Generar comentario basado en score
            comentarios_positivos = [
                "Excelente servicio, muy satisfecho",
                "Personal muy amable y eficiente",
                "Proceso rápido y sin complicaciones",
                "Superó mis expectativas",
                "Definitivamente recomendaría este banco"
            ]
            
            comentarios_neutros = [
                "Servicio aceptable, cumple lo básico",
                "Sin problemas pero nada extraordinario",
                "Proceso estándar, podría mejorar",
                "Servicio promedio"
            ]
            
            comentarios_negativos = [
                "Tiempo de espera excesivo",
                "Personal poco capacitado",
                "Proceso muy burocrático",
                "Mala experiencia, consideraré cambiar de banco",
                "Servicio deficiente, muchas complicaciones"
            ]
            
            if categoria == 'promotor':
                comentario = random.choice(comentarios_positivos)
            elif categoria == 'neutro':
                comentario = random.choice(comentarios_neutros)
            else:
                comentario = random.choice(comentarios_negativos)
            
            survey = {
                'encuesta_id': f'NPS-{i+1:06d}',
                'fecha_encuesta': survey_date,
                'cliente_id': f'CLI-{random.randint(1000, 99999):05d}',
                'nps_score': nps_score,
                'categoria_nps': categoria,
                'comentario': comentario,
                'banco': random.choice(self.banks),
                'canal_encuesta': random.choice(['email', 'sms', 'app', 'web']),
                'tiempo_respuesta_dias': random.randint(1, 30)
            }
            
            surveys.append(survey)
        
        df = pd.DataFrame(surveys)
        self.logger.info(f"Generadas {len(df)} encuestas NPS exitosamente")
        return df
    
    def generate_customer_reviews(self, num_reviews: int = 3000) -> pd.DataFrame:
        """
        Generar reviews de clientes en línea.
        
        Args:
            num_reviews: Número de reviews a generar
            
        Returns:
            DataFrame con reviews de clientes
        """
        self.logger.info(f"Generando {num_reviews} reviews de clientes...")
        
        reviews = []
        start_date = datetime.now() - timedelta(days=730)  # 2 años
        
        # Templates de reviews por calificación
        reviews_5_stars = [
            "Excelente banco, {banco} siempre cumple mis expectativas. El servicio en {canal} es excepcional.",
            "Muy satisfecho con {banco}. Personal profesional y procesos eficientes.",
            "Llevo años como cliente de {banco} y siempre me han dado un servicio de primera calidad.",
            "Recomiendo ampliamente {banco}. Excelente atención al cliente y productos competitivos."
        ]
        
        reviews_4_stars = [
            "Buen servicio en {banco}. Algunas mejoras en tiempos de espera serían apreciadas.",
            "En general satisfecho con {banco}. El servicio de {canal} es bueno pero podría ser más rápido.",
            "Banco confiable. {banco} tiene buenos productos aunque los costos podrían ser menores."
        ]
        
        reviews_3_stars = [
            "Servicio promedio en {banco}. Cumple lo básico pero nada extraordinario.",
            "Regular experiencia con {banco}. Hay aspectos que podrían mejorar significativamente.",
            "Servicio aceptable pero esperaba más de {banco}."
        ]
        
        reviews_2_stars = [
            "Mal servicio en {banco}. Tiempos de espera excesivos y personal poco capacitado.",
            "Decepcionado con {banco}. El servicio de {canal} es muy deficiente.",
            "Problemas frecuentes con {banco}. Considerando cambiar de entidad financiera."
        ]
        
        reviews_1_star = [
            "Pésimo servicio. {banco} no resuelve los problemas y el personal es incompetente.",
            "Muy mala experiencia con {banco}. Eviten a toda costa este banco.",
            "El peor banco. {banco} tiene un servicio al cliente deplorable."
        ]
        
        review_templates = {
            5: reviews_5_stars,
            4: reviews_4_stars,
            3: reviews_3_stars,
            2: reviews_2_stars,
            1: reviews_1_star
        }
        
        for i in range(num_reviews):
            review_date = start_date + timedelta(
                days=random.randint(0, 730)
            )
            
            # Distribución de calificaciones (sesgada hacia valores medios/altos)
            rating = random.choices(
                [1, 2, 3, 4, 5],
                weights=[10, 15, 25, 30, 20]
            )[0]
            
            banco = random.choice(self.banks)
            canal = random.choice(self.channels)
            
            # Seleccionar template y personalizar
            template = random.choice(review_templates[rating])
            review_text = template.format(banco=banco, canal=canal)
            
            review = {
                'review_id': f'REV-{i+1:06d}',
                'fecha_review': review_date,
                'autor': self.fake.name(),
                'banco': banco,
                'calificacion': rating,
                'texto_review': review_text,
                'plataforma': random.choice(['google', 'facebook', 'trustpilot', 'web_oficial']),
                'verificado': random.choices([True, False], weights=[70, 30])[0],
                'likes': random.randint(0, 50) if rating >= 4 else random.randint(0, 10),
                'respuesta_banco': random.choices([True, False], weights=[40, 60])[0]
            }
            
            reviews.append(review)
        
        df = pd.DataFrame(reviews)
        self.logger.info(f"Generadas {len(df)} reviews exitosamente")
        return df
    
    def generate_conversation_transcripts(self, num_transcripts: int = 1000) -> pd.DataFrame:
        """
        Generar transcripciones sintéticas de conversaciones.
        
        Args:
            num_transcripts: Número de transcripciones a generar
            
        Returns:
            DataFrame con transcripciones
        """
        self.logger.info(f"Generando {num_transcripts} transcripciones...")
        
        # Plantillas de conversaciones
        conversation_templates = {
            'consulta_saldo': [
                "Cliente: Hola, necesito consultar mi saldo",
                "Agente: Buenos días, con gusto le ayudo. ¿Me puede proporcionar su número de cuenta?",
                "Cliente: Sí, es {numero_cuenta}",
                "Agente: Perfecto, su saldo actual es ${saldo}. ¿Hay algo más en lo que pueda ayudarle?",
                "Cliente: No, eso es todo. Gracias",
                "Agente: De nada, que tenga un excelente día"
            ],
            'problema_tarjeta': [
                "Cliente: Mi tarjeta fue rechazada en un comercio",
                "Agente: Lamento escuchar eso. ¿Me puede dar los últimos 4 dígitos de su tarjeta?",
                "Cliente: {digitos_tarjeta}",
                "Agente: Veo que hay una retención por seguridad. Procedo a liberarla",
                "Cliente: ¿Ya puedo usarla?",
                "Agente: Sí, en unos minutos estará habilitada nuevamente"
            ],
            'reclamo_cargo': [
                "Cliente: Tengo un cargo que no reconozco por ${monto}",
                "Agente: Entiendo su preocupación. ¿Recuerda haber hecho alguna compra el {fecha}?",
                "Cliente: No, definitivamente no hice esa transacción",
                "Agente: Procederé a generar el reclamo. Le daré seguimiento en 3-5 días hábiles",
                "Cliente: ¿Mientras tanto qué pasa con el dinero?",
                "Agente: Se hará el reembolso provisional mientras investigamos"
            ]
        }
        
        transcripts = []
        
        for i in range(num_transcripts):
            # Seleccionar tipo de conversación
            conversation_type = random.choice(list(conversation_templates.keys()))
            template = conversation_templates[conversation_type]
            
            # Generar datos específicos
            numero_cuenta = f"{random.randint(1000000000, 9999999999)}"
            saldo = f"{random.randint(1000, 50000):,}"
            digitos_tarjeta = f"{random.randint(1000, 9999)}"
            monto = f"{random.randint(50, 5000)}"
            fecha_trans = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%d/%m/%Y")
            
            # Formatear conversación
            conversation = []
            for line in template:
                formatted_line = line.format(
                    numero_cuenta=numero_cuenta,
                    saldo=saldo,
                    digitos_tarjeta=digitos_tarjeta,
                    monto=monto,
                    fecha=fecha_trans
                )
                conversation.append(formatted_line)
            
            # Generar métricas de la conversación
            sentiment_score = random.uniform(-1, 1)
            if sentiment_score > 0.3:
                sentiment = 'positivo'
                satisfaction = random.uniform(3.5, 5.0)
            elif sentiment_score > -0.3:
                sentiment = 'neutro'
                satisfaction = random.uniform(2.5, 3.5)
            else:
                sentiment = 'negativo'
                satisfaction = random.uniform(1.0, 2.5)
            
            transcript = {
                'transcript_id': f'TRANS-{i+1:06d}',
                'fecha_conversacion': datetime.now() - timedelta(days=random.randint(0, 365)),
                'ticket_id': f'TKT-{random.randint(1, 10000):06d}',
                'tipo_conversacion': conversation_type,
                'transcript_texto': '\n'.join(conversation),
                'duracion_minutos': len(conversation) * random.uniform(0.5, 2.0),
                'sentiment_score': round(sentiment_score, 3),
                'sentiment_categoria': sentiment,
                'satisfaccion_estimada': round(satisfaction, 1),
                'palabras_clave': random.sample([
                    'saldo', 'tarjeta', 'cuenta', 'problema', 'ayuda',
                    'reclamo', 'cargo', 'transferencia', 'bloqueo'
                ], k=random.randint(2, 4)),
                'agente_id': f'AGT-{random.randint(1, 100):03d}',
                'canal': random.choice(['telefono', 'chat'])
            }
            
            transcripts.append(transcript)
        
        df = pd.DataFrame(transcripts)
        self.logger.info(f"Generadas {len(df)} transcripciones exitosamente")
        return df
    
    def save_datasets(self, output_dir: str = "data/simulated"):
        """
        Generar y guardar todos los datasets.
        
        Args:
            output_dir: Directorio de salida
        """
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Generar datasets
        tickets_df = self.generate_customer_tickets(10000)
        nps_df = self.generate_nps_surveys(5000)
        reviews_df = self.generate_customer_reviews(3000)
        transcripts_df = self.generate_conversation_transcripts(1000)
        
        # Guardar en múltiples formatos
        datasets = {
            'customer_tickets': tickets_df,
            'nps_surveys': nps_df,
            'customer_reviews': reviews_df,
            'conversation_transcripts': transcripts_df
        }
        
        for name, df in datasets.items():
            # CSV
            csv_path = os.path.join(output_dir, f'{name}.csv')
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            # Parquet (mejor para big data)
            parquet_path = os.path.join(output_dir, f'{name}.parquet')
            df.to_parquet(parquet_path, index=False)
            
            # JSON para APIs
            json_path = os.path.join(output_dir, f'{name}.json')
            df.to_json(json_path, orient='records', date_format='iso', indent=2)
            
            self.logger.info(f"Dataset '{name}' guardado en {output_dir}")
        
        # Generar metadata
        metadata = {
            'generacion_fecha': datetime.now().isoformat(),
            'total_registros': sum(len(df) for df in datasets.values()),
            'datasets': {
                name: {
                    'registros': len(df),
                    'columnas': list(df.columns),
                    'fecha_inicio': df.iloc[0]['fecha_creacion'].isoformat() if 'fecha_creacion' in df.columns else None,
                    'fecha_fin': df.iloc[-1]['fecha_creacion'].isoformat() if 'fecha_creacion' in df.columns else None
                } for name, df in datasets.items()
            }
        }
        
        metadata_path = os.path.join(output_dir, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Generación completa. {sum(len(df) for df in datasets.values())} registros en total")


def main():
    """Función principal para ejecutar el simulador."""
    parser = argparse.ArgumentParser(description='Generador de datos sintéticos de satisfacción del cliente')
    parser.add_argument('--tickets', type=int, default=10000, help='Número de tickets a generar')
    parser.add_argument('--nps', type=int, default=5000, help='Número de encuestas NPS a generar')
    parser.add_argument('--reviews', type=int, default=3000, help='Número de reviews a generar')
    parser.add_argument('--transcripts', type=int, default=1000, help='Número de transcripciones a generar')
    parser.add_argument('--output', type=str, default='data/simulated', help='Directorio de salida')
    parser.add_argument('--seed', type=int, default=42, help='Semilla para reproducibilidad')
    
    args = parser.parse_args()
    
    # Crear simulador
    simulator = CustomerSatisfactionDataSimulator(seed=args.seed)
    
    # Generar datasets con parámetros personalizados
    simulator.save_datasets(args.output)
    
    print(f"\n✅ Generación completada exitosamente!")
    print(f"📂 Archivos guardados en: {args.output}")
    print(f"📊 Total de registros generados: {args.tickets + args.nps + args.reviews + args.transcripts}")


if __name__ == "__main__":
    main() 