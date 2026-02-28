@echo off
echo Configurando ambiente virtual...
if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo Iniciando Aplicacao...
set PYTHONPATH=.
streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0

pause
