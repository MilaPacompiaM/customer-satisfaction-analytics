"""
Archivo principal para deployment en Streamlit Cloud.
Este archivo está en el root del repositorio para que Streamlit Cloud lo pueda encontrar.
"""

# Importar y ejecutar la aplicación desde el subdirectorio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar todas las funciones necesarias
try:
    # Importar todo el módulo
    from analytics.streamlit_dashboard import app
    
    # Ejecutar la función main
    if __name__ == "__main__":
        app.main()
    else:
        # Si se ejecuta como módulo de Streamlit
        app.main()
        
except ImportError as e:
    import streamlit as st
    st.error(f"Error importando la aplicación: {e}")
    st.info("Asegúrate de que el archivo analytics/streamlit_dashboard/app.py existe")
