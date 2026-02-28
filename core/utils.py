import re
from datetime import datetime

MONTHS_MAP = {
    'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4,
    'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8,
    'set': 9, 'out': 10, 'nov': 11, 'dez': 12
}

def parse_pt_br_number(text: str) -> float | None:
    """Converte string de número pt-BR (-4.172,94) para float."""
    if not text:
        return None
    try:
        # Remove pontos de milhar e troca vírgula por ponto
        clean_text = text.replace('.', '').replace(',', '.')
        return float(clean_text)
    except ValueError:
        return None

def format_date_br(day: str, month_str: str, year: int) -> str:
    """Formata dd, mon, yyyy para dd/mm/yyyy."""
    month = MONTHS_MAP.get(month_str.lower(), 1)
    return f"{int(day):02d}/{month:02d}/{year}"

def sanitize_filename(name: str) -> str:
    """Remove extensiva e caracteres especiais do nome do arquivo."""
    name = re.sub(r'\.pdf$', '', name, flags=re.IGNORECASE)
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
