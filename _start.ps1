Write-Host "Configurando ambiente virtual..." -ForegroundColor Cyan
if (!(Test-Path venv)) {
    python -m venv venv
}

. venv\Scripts\Activate.ps1

Write-Host "Instalando dependencias..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "Iniciando Aplicacao..." -ForegroundColor Green
$env:PYTHONPATH = "."
streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0
