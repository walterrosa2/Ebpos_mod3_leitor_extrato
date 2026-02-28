# Leitor de Extrato Itaú — MVP v1.0.0

Aplicação Streamlit para extrair lançamentos de extratos bancários do Itaú (PDF com texto selecionável) e exportar para Excel (.xlsx).

---

## 🔐 Credenciais
| Campo | Valor |
|-------|-------|
| Usuário | `admin` |
| Senha | `admin` |

---

## 🚀 Como Executar

### Windows (PowerShell)
```powershell
.\_start.ps1
```

### Windows (Prompt de Comando)
```bat
_start.bat
```

### Linux / Mac
```bash
chmod +x _start.sh
./_start.sh
```

> A aplicação ficará disponível em **http://localhost:8501**

---

## 📦 Instalação Manual (sem scripts)
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
export PYTHONPATH=.    # Linux/Mac
# ou: $env:PYTHONPATH="."    # Windows PowerShell

streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🧪 Rodando os Testes
```bash
# Windows (com venv ativo)
venv\Scripts\pytest tests/ -v

# Linux (com venv ativo)
pytest tests/ -v
```

---

## 📁 Estrutura do Projeto
```
/
├── .streamlit/config.toml   # Configuração visual (não versionado)
├── app/
│   └── app.py               # Interface Streamlit
├── core/
│   ├── itau_parser.py       # Extração de dados do PDF
│   ├── excel_writer.py      # Geração do Excel
│   ├── logger.py            # Auditoria (Loguru + JSONL)
│   └── utils.py             # Helpers (data, moeda)
├── knowledge/               # Padrões técnicos do projeto
├── tests/
│   └── test_parser.py       # Testes unitários
├── logs/                    # Gerado em runtime (não versionado)
├── .env.example             # Template de variáveis
├── requirements.txt
├── CHANGELOG.md
├── _start.ps1               # Inicialização Windows (PowerShell)
├── _start.bat               # Inicialização Windows (Batch)
└── _start.sh                # Inicialização Linux/Mac
```

---

## 📝 Auditoria
Eventos são gravados em `logs/audit.jsonl`. Formato:
```json
{"timestamp": "...", "user": "admin", "action": "PDF_PROCESSING", "pdf_name": "...", "rows_extracted": 42, "status": "SUCCESS"}
```

---

## ⚠️ Limitações (v1.0.0)
- Apenas PDFs com texto selecionável (não funciona com PDFs escaneados).
- Suporte exclusivo ao layout Itaú.
- Autenticação local simples (não segura para produção pública).
