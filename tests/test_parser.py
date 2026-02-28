import pytest
import pandas as pd
from core.utils import parse_pt_br_number, format_date_br
from core.itau_parser import extract_year_from_text

def test_parse_pt_br_number():
    assert parse_pt_br_number("1.234,56") == 1234.56
    assert parse_pt_br_number("-50,00") == -50.0
    assert parse_pt_br_number("0,00") == 0.0
    assert parse_pt_br_number("") is None

def test_format_date_br():
    assert format_date_br("02", "jan", 2024) == "02/01/2024"
    assert format_date_br("31", "dez", 2023) == "31/12/2023"

def test_extract_year_from_text():
    text = "extrato mensal\nlançamentos período: 01/01/2024 até 31/01/2024\nmais texto"
    assert extract_year_from_text(text) == 2024
    
    text_no_year = "texto sem data"
    # Deve retornar o ano atual por fallback
    from datetime import datetime
    assert extract_year_from_text(text_no_year) == datetime.now().year
