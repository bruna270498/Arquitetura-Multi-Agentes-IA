from datetime import datetime
from agentes.registro import get_agente
from agentes.agente_orquestrador import extrair_agente
from services.session import (
    atualizar_interacao,
    ja_saudou,
    marcar_saudacao,
    sessoes
)

# Instâncias dos agentes
agente_orcamento = get_agente("orcamento")
agente_duvidas = get_agente("duvidas")
agente_agendamento = get_agente("agendamento")

# Saudação
def saudacao():
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia ☀️ Como posso te ajudar hoje?"
    elif hora < 18:
        return "Boa tarde 👋 Como posso te ajudar hoje?"
    else:
        return "Boa noite 🌙 Como posso te ajudar hoje?"


# Detecta saudação
def is_saudacao(msg):
    msg = msg.lower().strip()
    return msg in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]


# Extrai tool
def extrair_tool(response):
    try:
        parts = response.candidates[0].content.parts
        for part in parts:
            if hasattr(part, "function_call"):
                return part.function_call.name
    except Exception:
        pass

    return "duvidas"


# Executa agente
def executar_agente(nome_agente, msg, cliente_id):
    if nome_agente == "orcamento":
        return agente_orcamento.responder(msg, cliente_id)
    elif nome_agente == "agendamento":
        return agente_agendamento.responder(msg, cliente_id)
    elif nome_agente == "duvidas":
        return agente_duvidas.responder(msg, cliente_id)
    return "Desculpe, não consegui entender. Pode reformular?"

PALAVRAS_AGENDAMENTO = ["agendar visita", "quero agendar", "agendar serviço", "marcar visita", "visita técnica"]
PALAVRAS_CONFIRMA = ["sim", "confirmo", "pode agendar", "quero agendar", "agendar"]

def processar_chat(mensagem, cliente_id):
    mensagem = mensagem.strip()
    msg_lower = mensagem.lower()
    atualizar_interacao(cliente_id)

    if is_saudacao(mensagem) and not ja_saudou(cliente_id):
        marcar_saudacao(cliente_id)
        return saudacao()

    if is_saudacao(mensagem):
        return "Como posso te ajudar?"

    if cliente_id not in sessoes:
        sessoes[cliente_id] = {}

    agente_atual = sessoes[cliente_id].get("agente_atual", "")

    # 1. Usuário pede visita diretamente → agendamento
    if any(p in msg_lower for p in PALAVRAS_AGENDAMENTO):
        sessoes[cliente_id]["agente_atual"] = "agendamento"
        return agente_agendamento.responder(mensagem, cliente_id)

    # 2. Veio do orçamento e confirmou → agendamento
    if agente_atual == "orcamento" and any(p in msg_lower for p in PALAVRAS_CONFIRMA):
        sessoes[cliente_id]["agente_atual"] = "agendamento"
        return agente_agendamento.responder(mensagem, cliente_id)

    # 3. Já está no agendamento → continua
    if agente_atual == "agendamento":
        return agente_agendamento.responder(mensagem, cliente_id)

    # 4. Orquestrador decide
    agente = extrair_agente(mensagem)
    sessoes[cliente_id]["agente_atual"] = agente
    return executar_agente(agente, mensagem, cliente_id)