"""
Analizador de sentimientos para comentarios y reviews de clientes.

Este módulo proporciona análisis de sentimientos usando múltiples técnicas:
- VADER Sentiment Analysis
- TextBlob
- Transformers (BERT, RoBERTa)
- Análisis de emociones
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# NLP Libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer

# Sentiment Analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Advanced NLP
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers no disponible. Usar pip install transformers")

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud

# Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib


class SentimentAnalyzer:
    """Analizador de sentimientos multimodal para textos de clientes."""
    
    def __init__(self, language: str = 'spanish'):
        """
        Inicializar el analizador de sentimientos.
        
        Args:
            language: Idioma para el análisis ('spanish' o 'english')
        """
        self.language = language
        self.logger = logging.getLogger(__name__)
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        
        # Inicializar componentes
        self._setup_nltk()
        self._setup_analyzers()
        
        # Patrones para cleaning
        self.cleaning_patterns = {
            'email': r'\S+@\S+',
            'url': r'http\S+|www\S+',
            'mention': r'@\w+',
            'hashtag': r'#\w+',
            'special_chars': r'[^a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s]',
            'multiple_spaces': r'\s+',
            'numbers': r'\d+'
        }
        
        # Palabras específicas del dominio bancario
        self.banking_positive_words = [
            'excelente', 'rápido', 'eficiente', 'profesional', 'amable',
            'resuelto', 'satisfecho', 'recomiendo', 'fácil', 'conveniente'
        ]
        
        self.banking_negative_words = [
            'lento', 'complicado', 'problema', 'error', 'demora',
            'malo', 'terrible', 'pésimo', 'frustrado', 'molesto'
        ]
    
    def _setup_nltk(self):
        """Configurar recursos de NLTK."""
        try:
            # Descargar recursos necesarios
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            
            # Configurar stopwords
            if self.language == 'spanish':
                self.stop_words = set(stopwords.words('spanish'))
                self.stemmer = SnowballStemmer('spanish')
            else:
                self.stop_words = set(stopwords.words('english'))
                self.stemmer = SnowballStemmer('english')
                
            self.logger.info("NLTK configurado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error configurando NLTK: {e}")
    
    def _setup_analyzers(self):
        """Configurar analizadores de sentimientos."""
        try:
            # VADER
            self.vader_analyzer = SentimentIntensityAnalyzer()
            
            # Transformers (si está disponible)
            if TRANSFORMERS_AVAILABLE:
                # Modelo en español para análisis de sentimientos
                self.transformer_sentiment = pipeline(
                    "sentiment-analysis",
                    model="nlptown/bert-base-multilingual-uncased-sentiment",
                    tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
                )
                
                # Modelo para análisis de emociones
                self.transformer_emotion = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    tokenizer="j-hartmann/emotion-english-distilroberta-base"
                )
            
            self.logger.info("Analizadores configurados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error configurando analizadores: {e}")
    
    def clean_text(self, text: str) -> str:
        """
        Limpiar y normalizar texto.
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        if not isinstance(text, str):
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Aplicar patrones de limpieza
        for pattern_name, pattern in self.cleaning_patterns.items():
            if pattern_name == 'multiple_spaces':
                text = re.sub(pattern, ' ', text)
            else:
                text = re.sub(pattern, '', text)
        
        # Eliminar espacios extra
        text = text.strip()
        
        return text
    
    def extract_features(self, text: str) -> Dict:
        """
        Extraer características del texto.
        
        Args:
            text: Texto para analizar
            
        Returns:
            Diccionario con características
        """
        features = {}
        
        # Características básicas
        features['length'] = len(text)
        features['word_count'] = len(text.split())
        features['sentence_count'] = len(sent_tokenize(text))
        features['avg_word_length'] = np.mean([len(word) for word in text.split()])
        
        # Conteos de puntuación
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['uppercase_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        # Palabras específicas del dominio
        text_lower = text.lower()
        features['positive_words'] = sum(1 for word in self.banking_positive_words if word in text_lower)
        features['negative_words'] = sum(1 for word in self.banking_negative_words if word in text_lower)
        
        return features
    
    def vader_analysis(self, text: str) -> Dict:
        """
        Análisis de sentimientos con VADER.
        
        Args:
            text: Texto para analizar
            
        Returns:
            Diccionario con scores VADER
        """
        scores = self.vader_analyzer.polarity_scores(text)
        
        # Categorizar sentimiento
        if scores['compound'] >= 0.05:
            category = 'positivo'
        elif scores['compound'] <= -0.05:
            category = 'negativo'
        else:
            category = 'neutro'
        
        return {
            'vader_compound': scores['compound'],
            'vader_positive': scores['pos'],
            'vader_neutral': scores['neu'],
            'vader_negative': scores['neg'],
            'vader_category': category
        }
    
    def textblob_analysis(self, text: str) -> Dict:
        """
        Análisis de sentimientos con TextBlob.
        
        Args:
            text: Texto para analizar
            
        Returns:
            Diccionario con scores TextBlob
        """
        blob = TextBlob(text)
        
        # Categorizar sentimiento
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            category = 'positivo'
        elif polarity < -0.1:
            category = 'negativo'
        else:
            category = 'neutro'
        
        return {
            'textblob_polarity': polarity,
            'textblob_subjectivity': blob.sentiment.subjectivity,
            'textblob_category': category
        }
    
    def transformer_analysis(self, text: str) -> Dict:
        """
        Análisis con modelos Transformer.
        
        Args:
            text: Texto para analizar
            
        Returns:
            Diccionario con resultados de transformers
        """
        if not TRANSFORMERS_AVAILABLE:
            return {}
        
        try:
            # Truncar texto si es muy largo
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]
            
            # Análisis de sentimientos
            sentiment_result = self.transformer_sentiment(text)[0]
            
            # Análisis de emociones (solo en inglés)
            emotion_result = {}
            if self.language == 'english':
                emotion_result = self.transformer_emotion(text)[0]
            
            return {
                'transformer_sentiment_label': sentiment_result['label'],
                'transformer_sentiment_score': sentiment_result['score'],
                'transformer_emotion_label': emotion_result.get('label', ''),
                'transformer_emotion_score': emotion_result.get('score', 0.0)
            }
            
        except Exception as e:
            self.logger.error(f"Error en análisis transformer: {e}")
            return {}
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis completo de sentimientos.
        
        Args:
            text: Texto para analizar
            
        Returns:
            Diccionario con todos los análisis
        """
        if not text or text.strip() == "":
            return {}
        
        # Limpiar texto
        clean_text = self.clean_text(text)
        
        # Extraer características
        features = self.extract_features(text)
        
        # Análisis de sentimientos
        vader_results = self.vader_analysis(clean_text)
        textblob_results = self.textblob_analysis(clean_text)
        transformer_results = self.transformer_analysis(clean_text)
        
        # Combinar resultados
        results = {
            'original_text': text,
            'clean_text': clean_text,
            'analysis_timestamp': datetime.now().isoformat(),
            **features,
            **vader_results,
            **textblob_results,
            **transformer_results
        }
        
        # Calcular sentimiento consenso
        results['consensus_sentiment'] = self._calculate_consensus_sentiment(results)
        
        return results
    
    def _calculate_consensus_sentiment(self, results: Dict) -> str:
        """
        Calcular sentimiento de consenso basado en múltiples análisis.
        
        Args:
            results: Resultados de análisis
            
        Returns:
            Sentimiento de consenso
        """
        sentiment_votes = []
        
        # Votos de VADER
        if 'vader_category' in results:
            sentiment_votes.append(results['vader_category'])
        
        # Votos de TextBlob
        if 'textblob_category' in results:
            sentiment_votes.append(results['textblob_category'])
        
        # Voto de características
        positive_words = results.get('positive_words', 0)
        negative_words = results.get('negative_words', 0)
        
        if positive_words > negative_words:
            sentiment_votes.append('positivo')
        elif negative_words > positive_words:
            sentiment_votes.append('negativo')
        else:
            sentiment_votes.append('neutro')
        
        # Determinar consenso por mayoría
        if not sentiment_votes:
            return 'neutro'
        
        vote_counts = {
            'positivo': sentiment_votes.count('positivo'),
            'negativo': sentiment_votes.count('negativo'),
            'neutro': sentiment_votes.count('neutro')
        }
        
        return max(vote_counts, key=vote_counts.get)
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """
        Analizar sentimientos en un DataFrame.
        
        Args:
            df: DataFrame con textos
            text_column: Nombre de la columna con texto
            
        Returns:
            DataFrame con análisis de sentimientos
        """
        self.logger.info(f"Analizando {len(df)} textos...")
        
        # Crear una copia del DataFrame
        result_df = df.copy()
        
        # Analizar cada texto
        analysis_results = []
        for idx, text in enumerate(df[text_column]):
            if idx % 100 == 0:
                self.logger.info(f"Procesado {idx}/{len(df)} textos")
            
            analysis = self.analyze_text(str(text))
            analysis_results.append(analysis)
        
        # Convertir resultados a DataFrame y combinar
        analysis_df = pd.DataFrame(analysis_results)
        
        # Combinar con DataFrame original
        for col in analysis_df.columns:
            if col not in ['original_text', 'clean_text']:
                result_df[f'sentiment_{col}'] = analysis_df[col]
        
        self.logger.info("Análisis completado")
        return result_df
    
    def generate_sentiment_report(self, df: pd.DataFrame) -> Dict:
        """
        Generar reporte de análisis de sentimientos.
        
        Args:
            df: DataFrame con análisis completo
            
        Returns:
            Diccionario con estadísticas del reporte
        """
        report = {}
        
        # Estadísticas generales
        total_texts = len(df)
        report['total_texts'] = total_texts
        
        # Distribución de sentimientos
        if 'sentiment_consensus_sentiment' in df.columns:
            sentiment_counts = df['sentiment_consensus_sentiment'].value_counts()
            report['sentiment_distribution'] = sentiment_counts.to_dict()
            report['sentiment_percentages'] = (sentiment_counts / total_texts * 100).to_dict()
        
        # Estadísticas de scores
        if 'sentiment_vader_compound' in df.columns:
            report['vader_stats'] = {
                'mean': df['sentiment_vader_compound'].mean(),
                'std': df['sentiment_vader_compound'].std(),
                'min': df['sentiment_vader_compound'].min(),
                'max': df['sentiment_vader_compound'].max()
            }
        
        if 'sentiment_textblob_polarity' in df.columns:
            report['textblob_stats'] = {
                'mean': df['sentiment_textblob_polarity'].mean(),
                'std': df['sentiment_textblob_polarity'].std(),
                'min': df['sentiment_textblob_polarity'].min(),
                'max': df['sentiment_textblob_polarity'].max()
            }
        
        # Características de texto
        if 'sentiment_length' in df.columns:
            report['text_stats'] = {
                'avg_length': df['sentiment_length'].mean(),
                'avg_word_count': df['sentiment_word_count'].mean(),
                'avg_sentence_count': df['sentiment_sentence_count'].mean()
            }
        
        return report
    
    def visualize_sentiment_distribution(self, df: pd.DataFrame, save_path: Optional[str] = None):
        """
        Visualizar distribución de sentimientos.
        
        Args:
            df: DataFrame con análisis
            save_path: Ruta para guardar la visualización
        """
        if 'sentiment_consensus_sentiment' not in df.columns:
            self.logger.error("No se encontró columna de sentimientos")
            return
        
        # Crear figura con subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Distribución de sentimientos
        sentiment_counts = df['sentiment_consensus_sentiment'].value_counts()
        ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
        ax1.set_title('Distribución de Sentimientos')
        
        # 2. VADER compound scores
        if 'sentiment_vader_compound' in df.columns:
            ax2.hist(df['sentiment_vader_compound'], bins=30, alpha=0.7, color='skyblue')
            ax2.axvline(df['sentiment_vader_compound'].mean(), color='red', linestyle='--', label='Media')
            ax2.set_xlabel('VADER Compound Score')
            ax2.set_ylabel('Frecuencia')
            ax2.set_title('Distribución VADER Compound Scores')
            ax2.legend()
        
        # 3. TextBlob polarity
        if 'sentiment_textblob_polarity' in df.columns:
            ax3.hist(df['sentiment_textblob_polarity'], bins=30, alpha=0.7, color='lightgreen')
            ax3.axvline(df['sentiment_textblob_polarity'].mean(), color='red', linestyle='--', label='Media')
            ax3.set_xlabel('TextBlob Polarity')
            ax3.set_ylabel('Frecuencia')
            ax3.set_title('Distribución TextBlob Polarity')
            ax3.legend()
        
        # 4. Longitud de texto por sentimiento
        if 'sentiment_length' in df.columns:
            df.boxplot(column='sentiment_length', by='sentiment_consensus_sentiment', ax=ax4)
            ax4.set_title('Longitud de Texto por Sentimiento')
            ax4.set_xlabel('Sentimiento')
            ax4.set_ylabel('Longitud de Texto')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Visualización guardada en: {save_path}")
        
        plt.show()
    
    def generate_wordcloud(self, df: pd.DataFrame, sentiment: str = 'all', 
                          save_path: Optional[str] = None):
        """
        Generar nube de palabras.
        
        Args:
            df: DataFrame con análisis
            sentiment: Sentimiento específico o 'all'
            save_path: Ruta para guardar la imagen
        """
        # Filtrar por sentimiento si se especifica
        if sentiment != 'all' and 'sentiment_consensus_sentiment' in df.columns:
            filtered_df = df[df['sentiment_consensus_sentiment'] == sentiment]
        else:
            filtered_df = df
        
        if 'sentiment_clean_text' in filtered_df.columns:
            text_col = 'sentiment_clean_text'
        else:
            text_col = df.columns[0]  # Usar primera columna de texto
        
        # Combinar todos los textos
        all_text = ' '.join(filtered_df[text_col].astype(str))
        
        # Generar nube de palabras
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            stopwords=self.stop_words,
            max_words=100,
            colormap='viridis'
        ).generate(all_text)
        
        # Visualizar
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Nube de Palabras - Sentimiento: {sentiment.title()}', fontsize=16)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Nube de palabras guardada en: {save_path}")
        
        plt.show()
    
    def save_model(self, model_path: str):
        """
        Guardar configuración del analizador.
        
        Args:
            model_path: Ruta para guardar el modelo
        """
        model_config = {
            'language': self.language,
            'banking_positive_words': self.banking_positive_words,
            'banking_negative_words': self.banking_negative_words,
            'cleaning_patterns': self.cleaning_patterns
        }
        
        joblib.dump(model_config, model_path)
        self.logger.info(f"Configuración guardada en: {model_path}")


def main():
    """Función principal para testing."""
    # Crear analizador
    analyzer = SentimentAnalyzer(language='spanish')
    
    # Textos de ejemplo
    sample_texts = [
        "Excelente servicio, muy satisfecho con la atención",
        "El proceso fue muy lento y complicado",
        "Servicio normal, nada extraordinario",
        "¡Terrible experiencia! Nunca más vuelvo",
        "Rápido y eficiente, recomiendo este banco"
    ]
    
    # Crear DataFrame de ejemplo
    df = pd.DataFrame({'comentario': sample_texts})
    
    # Analizar sentimientos
    result_df = analyzer.analyze_dataframe(df, 'comentario')
    
    # Generar reporte
    report = analyzer.generate_sentiment_report(result_df)
    
    print("=== Reporte de Análisis de Sentimientos ===")
    print(f"Total de textos: {report['total_texts']}")
    print(f"Distribución: {report['sentiment_distribution']}")
    print(f"Porcentajes: {report['sentiment_percentages']}")
    
    # Mostrar resultados
    print("\n=== Resultados Detallados ===")
    for idx, row in result_df.iterrows():
        print(f"\nTexto: {row['comentario']}")
        print(f"Sentimiento: {row['sentiment_consensus_sentiment']}")
        print(f"VADER: {row['sentiment_vader_compound']:.3f}")
        print(f"TextBlob: {row['sentiment_textblob_polarity']:.3f}")


if __name__ == "__main__":
    main() 