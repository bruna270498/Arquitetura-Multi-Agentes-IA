from agente_orcamento import AgenteOrcamento
from agente_agendamento import AgenteAgendamento
from agente_duvidas import AgenteDuvidas
from agente_orquestrador import agente_orquestrador

# Instâncias únicas (singleton simples)
agente_orcamento = AgenteOrcamento()
agente_agendamento = AgenteAgendamento()
agente_duvidas = AgenteDuvidas()


# Função para pegar agente dinamicamente
def get_agente(nome):
    agentes = {
        "orcamento": agente_orcamento,
        "agendamento": agente_agendamento,
        "duvidas": agente_duvidas,
        "orquestrador": agente_orquestrador
    }

    return agentes.get(nome)