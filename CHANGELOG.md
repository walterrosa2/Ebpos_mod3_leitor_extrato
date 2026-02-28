# Changelog — Leitor de Extrato Itaú

Todas as mudanças notáveis seguem a especificação [Conventional Commits](https://www.conventionalcommits.org/).

---

## [1.0.0] — 2026-02-28

### feat: MVP completo - Extrator de Extrato Itaú

**Funcionalidades:**
- Autenticação simples (admin/admin) via Streamlit session_state.
- Upload de múltiplos PDFs do Itaú (texto selecionável).
- Parsing automático: extração de Data, Histórico, Valor, Tipo e Saldo.
- Remoção automática do token `ag/origem` do histórico.
- Diferenciação automática: linhas de `SALDO` vs lançamentos comuns.
- Exportação para `.xlsx` por PDF (formatação BRL e datas dd/mm/yyyy).
- Geração de `.zip` consolidado para múltiplos PDFs.
- Editor de dados em tela (`st.data_editor`) para correções pré-exportação.
- Logs de auditoria em `logs/audit.jsonl` (Loguru).

**Interface:**
- Design dark mode com tema Itaú (Laranja + Vermelho Claro).
- Scripts de inicialização para Windows: `_start.ps1` e `_start.bat`.

**Correções de bugs:**
- `ModuleNotFoundError`: adicionados `__init__.py` e `PYTHONPATH=.` nos scripts.
- `'bytes' object has no attribute 'seek'`: corrigido via `io.BytesIO`.
