import sys
import os
import json
from loguru import logger
from datetime import datetime

# Garante que a pasta log existe
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configuração do Loguru
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")
logger.add(
    os.path.join(LOG_DIR, "app.log"),
    rotation="10 MB",
    retention="7 days",
    level="INFO"
)

# Arquivo JSONL para auditoria técnica
AUDIT_FILE = os.path.join(LOG_DIR, "audit.jsonl")

def log_event(user: str, pdf_name: str, xlsx_name: str | None, row_count: int | None, status: str, message: str | None = None) -> None:
    """Registra um evento de auditoria no sistema."""
    event = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "action": "PDF_PROCESSING",
        "pdf_name": pdf_name,
        "xlsx_generated": xlsx_name,
        "rows_extracted": row_count,
        "status": status,
        "details": message
    }
    
    # Log textual
    log_msg = f"User: {user} | PDF: {pdf_name} | Status: {status} | Rows: {row_count}"
    if status == "SUCCESS":
        logger.info(log_msg)
    else:
        logger.error(f"{log_msg} | Error: {message}")
        
    # Auditoria JSONL
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"Falha ao gravar log de auditoria: {e}")
