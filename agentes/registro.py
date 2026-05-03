from .agente_orcamento import AgenteOrcamento
from .agente_agendamento import AgenteAgendamento
from .agente_duvidas import AgenteDuvidas

agente_orcamento   = AgenteOrcamento()
agente_agendamento = AgenteAgendamento()
agente_duvidas     = AgenteDuvidas()

def get_agente(nome):
    agentes = {
        "orcamento":   agente_orcamento,
        "agendamento": agente_agendamento,
        "duvidas":     agente_duvidas,
    }
    return agentes.get(nome)