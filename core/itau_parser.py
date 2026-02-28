import io
import pdfplumber
import pandas as pd
import re
from datetime import datetime
from core.utils import parse_pt_br_number, format_date_br, sanitize_filename
from core.logger import logger

def extract_year_from_text(text: str) -> int:
    """
    Busca no texto o padrão: lançamentos período: dd/mm/yyyy até dd/mm/yyyy
    Retorna o ano da data final.
    """
    pattern = r"lançamentos período: \d{2}/\d{2}/\d{4} até \d{2}/\d{2}/(\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return datetime.now().year

def parse_itau_pdf(pdf_bytes: bytes, pdf_name: str) -> pd.DataFrame:
    """
    Lê o PDF do Itaú e extrai os lançamentos.
    Lógica:
    1. Extrair todo o texto.
    2. Identificar o ano de referência.
    3. Identificar linhas que começam com "dd / mon".
    4. Processar cada linha para separar dados e remover ag/origem.
    """
    data_rows = []
    
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text() or ""
            
        year = extract_year_from_text(all_text)
        
        # Regex para capturar linhas de extrato: dd / mon histórico [ag/origem] valor_ou_saldo
        # Exemplo: 02 / jan SALDO ANTERIOR 1.234,56
        # Exemplo: 05 / jan COMPRA CARTAO 0940 -50,00
        line_pattern = r"^(\d{2})\s?/\s?([a-z]{3})\s+(.*)$"
        
        for line in all_text.split('\n'):
            line = line.strip()
            match = re.match(line_pattern, line, re.IGNORECASE)
            if not match:
                continue
            
            day = match.group(1)
            month_str = match.group(2)
            remainder = match.group(3)
            
            # Tokenizar o restante para achar o valor e o ag/origem
            tokens = remainder.split()
            if not tokens:
                continue
                
            # O último token é sempre o valor/saldo (em pt-BR)
            val_token = tokens[-1]
            value = parse_pt_br_number(val_token)
            
            # Verificar se o penúltimo token é ag/origem (digitos, 3-6 caracteres)
            historico_tokens = tokens[:-1]
            if len(historico_tokens) > 0:
                last_h_token = historico_tokens[-1]
                if last_h_token.isdigit() and 3 <= len(last_h_token) <= 6:
                    historico_tokens = historico_tokens[:-1]
            
            historico = " ".join(historico_tokens).strip()
            full_date = format_date_br(day, month_str, year)
            
            row = {
                "Data": full_date,
                "Histórico/Descrição": historico,
                "Valor": None,
                "Tipo": None,
                "Saldo após o lançamento": None
            }
            
            # Regras de SALDO vs LANÇAMENTO
            if historico.upper().startswith("SALDO"):
                row["Saldo após o lançamento"] = value
            else:
                row["Valor"] = value
                if value is not None:
                    row["Tipo"] = "Crédito" if value > 0 else "Débito"
            
            data_rows.append(row)
            
    df = pd.DataFrame(data_rows)
    # Garantir ordem das colunas
    cols = ["Data", "Histórico/Descrição", "Valor", "Tipo", "Saldo após o lançamento"]
    if df.empty:
        return pd.DataFrame(columns=cols)
    return df[cols]
