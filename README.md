# Meu Agente de IA

Projeto de estudo: construindo um agente de IA do zero.

## Como rodar
1. `pip install -r requirements.txt`
2. Crie um `.env` com `ANTHROPIC_API_KEY=...`
3. `python agent.py`

## Diário de evolução
- **v0.1** – Loop básico + ferramentas de hora e notas
- **v0.2** – Streaming: a resposta aparece em tempo real (`messages.stream`);
  tratamento de Ctrl+C no chat