#!/usr/bin/env bash
# _start.sh — Script de execução para Linux/Mac
set -e

echo "🔧 Configurando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Instalando dependências..."
pip install -r requirements.txt -q

echo "🚀 Iniciando Aplicação..."
export PYTHONPATH="."
streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0
