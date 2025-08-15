@echo off
echo 🚀 Iniciando Customer Satisfaction Analytics Dashboard...
echo.

REM Verificar si estamos en el directorio correcto
if not exist ".venv" (
    echo ❌ Error: No se encuentra el entorno virtual .venv
    echo Ejecuta este script desde el directorio raíz del proyecto
    pause
    exit /b 1
)

REM Activar el entorno virtual
echo 📦 Activando entorno virtual...
call .venv\Scripts\activate

REM Verificar instalación de Streamlit
echo 🔍 Verificando dependencias...
python -c "import streamlit; print('✅ Streamlit OK')" 2>nul || (
    echo ⚠️ Instalando dependencias...
    pip install -r requirements-streamlit.txt
)

REM Lanzar la aplicación
echo 🌐 Lanzando dashboard...
echo.
echo 📍 URL Local: http://localhost:8501
echo 📍 URL Red: http://192.168.18.15:8501
echo.
echo 💡 Para detener: Ctrl+C en esta ventana
echo.

python -m streamlit run streamlit_app.py --server.port 8501

pause
