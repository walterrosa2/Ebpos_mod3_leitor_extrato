#!/bin/bash
# Script para Linux/Docker

# Garante PYTHONPATH
export PYTHONPATH=.

# Inicia Streamlit
streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0
