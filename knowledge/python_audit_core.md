# Padrões de Auditoria e Logs

## Configuração Loguru
- Usar rotação diária e retenção de 7 dias.
- Formato JSONL para auditoria.

## Eventos de Auditoria
- Cada PDF processado deve gerar uma entrada.
- Campos: `timestamp`, `user`, `action`, `filename`, `rows`, `status`.
