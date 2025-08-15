# Customer Satisfaction Analytics - Dashboard Deployment

## 🚀 Deploy en Streamlit Cloud

### Pasos para Deploy

1. **Fork del Repositorio** (ya que eres colaborador):
   - Ve a: https://github.com/MilaPacompiaM/customer-satisfaction-analytics
   - Haz clic en "Fork" para crear una copia en tu cuenta

2. **Deploy en Streamlit Cloud**:
   - Ve a: https://share.streamlit.io/
   - Conecta tu cuenta de GitHub
   - Selecciona tu fork del repositorio
   - **Archivo principal**: `streamlit_app.py` (este está en la raíz)
   - **Requirements**: `requirements-streamlit.txt`

### URL del archivo principal para deploy:
```
https://github.com/TU_USUARIO/customer-satisfaction-analytics/blob/main/streamlit_app.py
```

## 🔧 Configuración Local

Para probar localmente:

```bash
# 1. Activar el entorno virtual
.venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements-streamlit.txt

# 3. Ejecutar la aplicación
streamlit run streamlit_app.py
```

## 📊 Características del Dashboard

- ✅ **Datos simulados**: Funciona sin conexión a AWS
- ✅ **Diseño mejorado**: Contraste y colores optimizados
- ✅ **Gráficos corregidos**: Sin errores de `update_xaxis`
- ✅ **Responsive**: Adaptable a diferentes pantallas
- ✅ **Deploy ready**: Configurado para Streamlit Cloud

## 🎨 Mejoras Implementadas

### Diseño Visual
- ✅ Fondo blanco con contraste adecuado
- ✅ Colores de texto oscuros (#333333)
- ✅ Bordes y sombras para mejor definición
- ✅ Gráficos con fondos blancos y grillas sutiles

### Correcciones Técnicas
- ✅ Reemplazado `fig.update_xaxis()` por `fig.update_layout(xaxis_tickangle=45)`
- ✅ Función `improve_chart_design()` aplicada a todos los gráficos
- ✅ Datos simulados como fallback para errores de AWS
- ✅ Manejo de errores robusto

### Estructura para Deploy
- ✅ `streamlit_app.py` en la raíz
- ✅ `requirements-streamlit.txt` mínimo
- ✅ Configuración `.streamlit/config.toml`

## 🌐 URLs de Deploy

- **Streamlit Cloud**: customer-satisfaction-analytics-[hash].streamlit.app
- **Local**: http://localhost:8501

## 🔍 Troubleshooting

### Si hay errores en deploy:
1. Verificar que el archivo sea `streamlit_app.py`
2. Usar `requirements-streamlit.txt` (no el general)
3. Verificar que el repositorio sea público
4. Esperar 2-3 minutos para el primer deploy

### Para desarrollo local:
- Usar el entorno virtual `.venv`
- Todos los errores de AWS se manejan automáticamente
- Los datos simulados aparecen con warning amarillo
