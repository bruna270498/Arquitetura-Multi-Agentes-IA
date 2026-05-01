from datetime import datetime
from agentes.registro import get_agente
from services.session import (
    atualizar_interacao,
    ja_saudou,
    marcar_saudacao
)

# Instâncias dos agentes
agente_orcamento = get_agente("orcamento")
agente_duvidas = get_agente("duvidas")
agente_agendamento = get_agente("agendamento")
agente_orquestrador = get_agente("orquestrador")

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
def executar_agente(nome_agente, msg):
    if nome_agente == "orcamento":
        return agente_orcamento.responder(msg)

    elif nome_agente == "agendamento":
        return agente_agendamento.responder(msg)

    elif nome_agente == "duvidas":
        return agente_duvidas.responder(msg)

    return "Desculpe, não consegui entender. Pode reformular?"


# Fluxo principal
def processar_chat(mensagem, cliente_id):

    mensagem = mensagem.strip()

    # 🔹 Atualiza sessão
    atualizar_interacao(cliente_id)

    # Saudação inteligente
    if is_saudacao(mensagem) and not ja_saudou(cliente_id):
        marcar_saudacao(cliente_id)
        return saudacao()

    if is_saudacao(mensagem):
        return "Como posso te ajudar?"

    # Orquestrador
    intent = agente_orquestrador.generate_content(mensagem)
    agente = extrair_tool(intent)

    # Executa agente
    return executar_agente(agente, mensagem)