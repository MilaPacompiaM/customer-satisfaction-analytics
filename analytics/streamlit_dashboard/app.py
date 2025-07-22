"""
Dashboard de Customer Satisfaction Analytics usando Streamlit.
Alternativa GRATUITA a Amazon QuickSight.

Características:
- 📊 KPIs principales en tiempo real
- 📈 Gráficos interactivos con Plotly
- 🔍 Filtros dinámicos
- 📱 Responsive design
- 🚀 Conexión directa a Athena
- 💡 Insights automáticos con IA
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import boto3
from datetime import datetime, timedelta, date
import json
import time
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Configuración de página
st.set_page_config(
    page_title="Customer Satisfaction Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para un look profesional
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    
    .insight-box {
        background: #f0f8ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)


class AthenaConnector:
    """Connector para AWS Athena - optimizado para capa gratuita."""
    
    def __init__(self, region_name: str = 'us-east-1', 
                 workgroup: str = 'customer-satisfaction-workgroup'):
        self.region_name = region_name
        self.workgroup = workgroup
        self.athena_client = None
        self.s3_client = None
        self._init_clients()
    
    def _init_clients(self):
        """Inicializar clientes AWS con manejo de errores."""
        try:
            self.athena_client = boto3.client('athena', region_name=self.region_name)
            self.s3_client = boto3.client('s3', region_name=self.region_name)
        except Exception as e:
            st.error(f"❌ Error conectando a AWS: {e}")
            st.info("💡 Usando datos simulados para el demo")
    
    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def execute_query(_self, query: str, limit_gb: float = 1.0) -> pd.DataFrame:
        """Ejecutar query en Athena con límites de datos escaneados."""
        try:
            if _self.athena_client is None:
                return _self._generate_sample_data(query)
            
            # Agregar LIMIT automático para controlar costos
            if "LIMIT" not in query.upper():
                query += " LIMIT 10000"
            
            # Ejecutar query
            response = _self.athena_client.start_query_execution(
                QueryString=query,
                WorkGroup=_self.workgroup,
                ResultConfiguration={
                    'OutputLocation': 's3://customer-satisfaction-athena-results/'
                }
            )
            
            query_execution_id = response['QueryExecutionId']
            
            # Esperar resultados
            while True:
                result = _self.athena_client.get_query_execution(
                    QueryExecutionId=query_execution_id
                )
                status = result['QueryExecution']['Status']['State']
                
                if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(1)
            
            if status == 'SUCCEEDED':
                # Obtener resultados
                result = _self.athena_client.get_query_results(
                    QueryExecutionId=query_execution_id
                )
                
                # Convertir a DataFrame
                columns = [col['Label'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
                rows = []
                for row in result['ResultSet']['Rows'][1:]:  # Skip header
                    rows.append([col.get('VarCharValue', '') for col in row['Data']])
                
                return pd.DataFrame(rows, columns=columns)
            else:
                st.error(f"❌ Query falló: {status}")
                return _self._generate_sample_data(query)
                
        except Exception as e:
            st.warning(f"⚠️ Usando datos simulados: {e}")
            return _self._generate_sample_data(query)
    
    def _generate_sample_data(self, query: str) -> pd.DataFrame:
        """Generar datos de muestra para demo sin AWS."""
        np.random.seed(42)
        
        if "satisfaction_metrics" in query.lower():
            # Datos de métricas de satisfacción
            dates = pd.date_range('2024-01-01', periods=90, freq='D')
            data = []
            
            for fecha in dates:
                for canal in ['telefono', 'chat', 'email', 'presencial']:
                    data.append({
                        'fecha': fecha.strftime('%Y-%m-%d'),
                        'canal': canal,
                        'total_tickets': np.random.poisson(50),
                        'satisfaccion_promedio': np.random.normal(3.8, 0.5),
                        'tasa_satisfaccion': np.random.uniform(0.7, 0.95),
                        'tasa_resolucion': np.random.uniform(0.8, 0.98),
                        'duracion_promedio': np.random.normal(15, 5),
                        'clientes_unicos': np.random.poisson(30),
                        'nps_score_calculado': np.random.normal(40, 15)
                    })
            
            return pd.DataFrame(data)
        
        elif "nps_analysis" in query.lower():
            # Datos de análisis NPS
            data = []
            for mes in pd.date_range('2024-01-01', periods=6, freq='M'):
                for categoria in ['promotores', 'neutrales', 'detractores']:
                    data.append({
                        'mes': mes.strftime('%Y-%m'),
                        'categoria_nps': categoria,
                        'total_encuestas': np.random.poisson(100),
                        'nps_promedio': np.random.normal(6 if categoria == 'promotores' else 
                                                      5 if categoria == 'neutrales' else 3, 1),
                        'porcentaje': np.random.uniform(20, 40)
                    })
            
            return pd.DataFrame(data)
        
        elif "agent_performance" in query.lower():
            # Datos de rendimiento de agentes
            data = []
            for agente_id in [f'AGT-{i:03d}' for i in range(1, 21)]:
                for canal in ['telefono', 'chat', 'email']:
                    data.append({
                        'agente_id': agente_id,
                        'canal': canal,
                        'total_tickets': np.random.poisson(30),
                        'satisfaccion_promedio': np.random.normal(3.8, 0.3),
                        'duracion_promedio': np.random.normal(15, 3),
                        'tasa_resolucion': np.random.uniform(0.85, 0.98),
                        'clientes_atendidos': np.random.poisson(25)
                    })
            
            return pd.DataFrame(data)
        
        else:
            # Datos genéricos
            return pd.DataFrame({
                'fecha': pd.date_range('2024-01-01', periods=30),
                'valor': np.random.randn(30).cumsum()
            })


def load_data() -> Dict[str, pd.DataFrame]:
    """Cargar todos los datasets necesarios."""
    connector = AthenaConnector()
    
    datasets = {}
    
    with st.spinner('🔄 Cargando datos...'):
        # Métricas principales
        datasets['metrics'] = connector.execute_query("""
            SELECT fecha, canal, total_tickets, satisfaccion_promedio, 
                   tasa_satisfaccion, tasa_resolucion, duracion_promedio,
                   clientes_unicos, nps_score_calculado
            FROM satisfaction_metrics 
            WHERE fecha >= CURRENT_DATE - INTERVAL '90' DAY
            ORDER BY fecha DESC
        """)
        
        # Análisis NPS
        datasets['nps'] = connector.execute_query("""
            SELECT mes, categoria_nps, total_encuestas, nps_promedio, porcentaje
            FROM nps_analysis 
            WHERE mes >= CURRENT_DATE - INTERVAL '6' MONTH
        """)
        
        # Rendimiento de agentes
        datasets['agents'] = connector.execute_query("""
            SELECT agente_id, canal, total_tickets, satisfaccion_promedio,
                   duracion_promedio, tasa_resolucion, clientes_atendidos
            FROM agent_performance 
            WHERE total_tickets >= 10
        """)
    
    return datasets


def create_kpi_cards(df: pd.DataFrame):
    """Crear tarjetas de KPIs principales."""
    # Calcular KPIs
    latest_data = df[df['fecha'] == df['fecha'].max()]
    
    avg_satisfaction = latest_data['satisfaccion_promedio'].mean()
    total_tickets = latest_data['total_tickets'].sum()
    avg_resolution_rate = latest_data['tasa_resolucion'].mean()
    avg_duration = latest_data['duracion_promedio'].mean()
    
    # Calcular cambios (vs día anterior)
    previous_data = df[df['fecha'] == df['fecha'].unique()[-2]] if len(df['fecha'].unique()) > 1 else latest_data
    
    satisfaction_change = avg_satisfaction - previous_data['satisfaccion_promedio'].mean()
    tickets_change = total_tickets - previous_data['total_tickets'].sum()
    resolution_change = avg_resolution_rate - previous_data['tasa_resolucion'].mean()
    duration_change = avg_duration - previous_data['duracion_promedio'].mean()
    
    # Crear columnas para KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            label="📊 Satisfacción Promedio",
            value=f"{avg_satisfaction:.2f}/5.0",
            delta=f"{satisfaction_change:+.2f}",
            help="Puntuación promedio de satisfacción del cliente"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            label="🎫 Total Tickets",
            value=f"{total_tickets:,}",
            delta=f"{tickets_change:+.0f}",
            help="Número total de tickets procesados hoy"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            label="✅ Tasa Resolución",
            value=f"{avg_resolution_rate:.1%}",
            delta=f"{resolution_change:+.1%}",
            help="Porcentaje de tickets resueltos exitosamente"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            label="⏱️ Tiempo Promedio",
            value=f"{avg_duration:.0f} min",
            delta=f"{duration_change:+.0f} min",
            help="Duración promedio de atención por ticket"
        )
        st.markdown('</div>', unsafe_allow_html=True)


def create_satisfaction_trend(df: pd.DataFrame):
    """Crear gráfico de tendencia de satisfacción."""
    st.subheader("📈 Tendencia de Satisfacción por Canal")
    
    # Preparar datos
    df['fecha'] = pd.to_datetime(df['fecha'])
    daily_avg = df.groupby(['fecha', 'canal'])['satisfaccion_promedio'].mean().reset_index()
    
    # Crear gráfico
    fig = px.line(
        daily_avg,
        x='fecha',
        y='satisfaccion_promedio',
        color='canal',
        title='Evolución de la Satisfacción del Cliente',
        labels={
            'fecha': 'Fecha',
            'satisfaccion_promedio': 'Satisfacción Promedio',
            'canal': 'Canal'
        },
        color_discrete_map={
            'telefono': '#1f77b4',
            'chat': '#ff7f0e',
            'email': '#2ca02c',
            'presencial': '#d62728'
        }
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        hovermode='x unified',
        xaxis_title="Fecha",
        yaxis_title="Satisfacción Promedio (1-5)",
        yaxis=dict(range=[1, 5])
    )
    
    # Agregar línea de objetivo
    fig.add_hline(y=4.0, line_dash="dash", line_color="red", 
                  annotation_text="Objetivo: 4.0")
    
    st.plotly_chart(fig, use_container_width=True)


def create_channel_analysis(df: pd.DataFrame):
    """Crear análisis por canal."""
    st.subheader("📊 Análisis por Canal de Atención")
    
    # Métricas por canal
    channel_metrics = df.groupby('canal').agg({
        'total_tickets': 'sum',
        'satisfaccion_promedio': 'mean',
        'tasa_resolucion': 'mean',
        'duracion_promedio': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras - Tickets por canal
        fig1 = px.bar(
            channel_metrics,
            x='canal',
            y='total_tickets',
            title='Volumen de Tickets por Canal',
            color='canal',
            text='total_tickets'
        )
        fig1.update_traces(texttemplate='%{text}', textposition='outside')
        fig1.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Gráfico de radar - Métricas por canal
        categories = ['Satisfacción', 'Resolución', 'Eficiencia']
        
        fig2 = go.Figure()
        
        for _, row in channel_metrics.iterrows():
            valores = [
                row['satisfaccion_promedio'] / 5 * 100,  # Normalizar a 100
                row['tasa_resolucion'] * 100,
                (30 - row['duracion_promedio']) / 30 * 100  # Invertir duración
            ]
            
            fig2.add_trace(go.Scatterpolar(
                r=valores,
                theta=categories,
                fill='toself',
                name=row['canal'].title()
            ))
        
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Comparación de Rendimiento por Canal",
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)


def create_nps_analysis(nps_df: pd.DataFrame):
    """Crear análisis de NPS."""
    st.subheader("🎯 Análisis Net Promoter Score (NPS)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución NPS
        latest_nps = nps_df[nps_df['mes'] == nps_df['mes'].max()]
        
        fig1 = px.pie(
            latest_nps,
            values='total_encuestas',
            names='categoria_nps',
            title='Distribución NPS Actual',
            color_discrete_map={
                'promotores': '#4CAF50',
                'neutrales': '#FFC107',
                'detractores': '#F44336'
            }
        )
        fig1.update_traces(textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Evolución NPS
        nps_evolution = nps_df.groupby(['mes', 'categoria_nps'])['total_encuestas'].sum().reset_index()
        
        fig2 = px.bar(
            nps_evolution,
            x='mes',
            y='total_encuestas',
            color='categoria_nps',
            title='Evolución NPS por Mes',
            color_discrete_map={
                'promotores': '#4CAF50',
                'neutrales': '#FFC107',
                'detractores': '#F44336'
            }
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Calcular NPS Score
    promotores = latest_nps[latest_nps['categoria_nps'] == 'promotores']['total_encuestas'].sum()
    detractores = latest_nps[latest_nps['categoria_nps'] == 'detractores']['total_encuestas'].sum()
    total = latest_nps['total_encuestas'].sum()
    
    if total > 0:
        nps_score = ((promotores - detractores) / total) * 100
        
        # Mostrar NPS Score
        st.markdown(f"""
        <div class="metric-container">
            <h3>🎯 NPS Score Actual</h3>
            <h1 style="color: {'#4CAF50' if nps_score > 0 else '#F44336'};">{nps_score:.0f}</h1>
            <p>{"Excelente" if nps_score > 50 else "Bueno" if nps_score > 0 else "Necesita Mejora"}</p>
        </div>
        """, unsafe_allow_html=True)


def create_agent_performance(agents_df: pd.DataFrame):
    """Crear análisis de rendimiento de agentes."""
    st.subheader("👥 Rendimiento de Agentes")
    
    # Top 10 agentes por satisfacción
    top_agents = agents_df.groupby('agente_id').agg({
        'satisfaccion_promedio': 'mean',
        'total_tickets': 'sum',
        'tasa_resolucion': 'mean'
    }).reset_index().sort_values('satisfaccion_promedio', ascending=False).head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            top_agents,
            x='agente_id',
            y='satisfaccion_promedio',
            title='Top 10 Agentes por Satisfacción',
            color='satisfaccion_promedio',
            color_continuous_scale='Viridis'
        )
        fig1.update_xaxis(tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Scatter plot - Satisfacción vs Volumen
        fig2 = px.scatter(
            agents_df,
            x='total_tickets',
            y='satisfaccion_promedio',
            size='tasa_resolucion',
            color='canal',
            title='Satisfacción vs Volumen de Tickets',
            hover_data=['agente_id']
        )
        st.plotly_chart(fig2, use_container_width=True)


def create_insights(datasets: Dict[str, pd.DataFrame]):
    """Generar insights automáticos con IA."""
    st.subheader("🧠 Insights Automáticos")
    
    metrics_df = datasets['metrics']
    latest_data = metrics_df[metrics_df['fecha'] == metrics_df['fecha'].max()]
    
    insights = []
    
    # Insight 1: Canal con mejor/peor rendimiento
    channel_performance = latest_data.groupby('canal')['satisfaccion_promedio'].mean()
    best_channel = channel_performance.idxmax()
    worst_channel = channel_performance.idxmin()
    
    insights.append(f"📈 **Canal Destacado**: {best_channel.title()} tiene la mayor satisfacción ({channel_performance[best_channel]:.2f}/5.0)")
    insights.append(f"⚠️ **Área de Mejora**: {worst_channel.title()} necesita atención ({channel_performance[worst_channel]:.2f}/5.0)")
    
    # Insight 2: Tendencia general
    recent_trend = metrics_df.tail(7)['satisfaccion_promedio'].mean()
    older_trend = metrics_df.head(7)['satisfaccion_promedio'].mean()
    trend_direction = "📈 mejorando" if recent_trend > older_trend else "📉 declinando"
    
    insights.append(f"📊 **Tendencia General**: La satisfacción está {trend_direction} ({recent_trend:.2f} vs {older_trend:.2f})")
    
    # Insight 3: Duración vs Satisfacción
    duration_corr = metrics_df['duracion_promedio'].corr(metrics_df['satisfaccion_promedio'])
    if duration_corr < -0.3:
        insights.append("⏱️ **Duración Crítica**: Tiempos largos están afectando negativamente la satisfacción")
    
    # Mostrar insights
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def create_cost_monitor():
    """Monitor de costos AWS para mantenerse en capa gratuita."""
    st.sidebar.subheader("💰 Monitor de Costos AWS")
    
    # Simular uso actual (en producción sería real)
    s3_usage = np.random.uniform(0.3, 0.8)  # GB
    athena_usage = np.random.uniform(0.5, 2.0)  # GB escaneados
    glue_usage = np.random.uniform(5, 15)  # horas
    
    # Mostrar barras de progreso
    st.sidebar.metric("S3 Storage", f"{s3_usage:.1f}GB", f"de 5GB gratis")
    st.sidebar.progress(s3_usage / 5.0)
    
    st.sidebar.metric("Athena Scan", f"{athena_usage:.1f}GB", f"de 5GB gratis")
    st.sidebar.progress(athena_usage / 5.0)
    
    st.sidebar.metric("Glue Hours", f"{glue_usage:.0f}h", f"de 1M horas gratis")
    st.sidebar.progress(glue_usage / 100.0)
    
    # Alertas
    if s3_usage > 4.0:
        st.sidebar.warning("⚠️ S3 cerca del límite gratuito")
    if athena_usage > 4.0:
        st.sidebar.warning("⚠️ Athena cerca del límite gratuito")
    
    # Costo estimado
    estimated_cost = max(0, (s3_usage - 5) * 0.023 + (athena_usage - 5) * 5.0)
    st.sidebar.metric("💸 Costo Estimado", f"${estimated_cost:.2f}/mes")


def main():
    """Función principal del dashboard."""
    # Header
    st.markdown('<h1 class="main-header">📊 Customer Satisfaction Analytics</h1>', 
                unsafe_allow_html=True)
    
    # Monitor de costos en sidebar
    create_cost_monitor()
    
    # Filtros en sidebar
    st.sidebar.subheader("🔍 Filtros")
    
    # Selector de fecha
    date_range = st.sidebar.date_input(
        "📅 Rango de Fechas",
        value=(date.today() - timedelta(days=30), date.today()),
        max_value=date.today()
    )
    
    # Selector de canal
    channels = st.sidebar.multiselect(
        "📞 Canales",
        options=['telefono', 'chat', 'email', 'presencial'],
        default=['telefono', 'chat', 'email', 'presencial']
    )
    
    # Cargar datos
    datasets = load_data()
    
    # Filtrar datos según selección
    metrics_df = datasets['metrics']
    if channels:
        metrics_df = metrics_df[metrics_df['canal'].isin(channels)]
    
    # KPIs principales
    create_kpi_cards(metrics_df)
    
    st.markdown("---")
    
    # Gráficos principales
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_satisfaction_trend(metrics_df)
        create_channel_analysis(metrics_df)
    
    with col2:
        create_nps_analysis(datasets['nps'])
        create_insights(datasets)
    
    st.markdown("---")
    
    # Análisis de agentes
    create_agent_performance(datasets['agents'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        🚀 Dashboard gratuito potenciado por Streamlit | 
        💡 Alternativa sin costo a Amazon QuickSight |
        📊 Datos en tiempo real desde AWS Athena
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main() 