from vertexai.generative_models import GenerativeModel

#Este é o cérebro do nossos agentes
agente_orquestrador = GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
    Você é um roteador de atendimento.
    Sua única função é escolher qual agente deve atender o usuário.

    Agentes disponíveis:
    - duvidas
    - orcamento
    - agendamento

    Regras:
    - Nunca responda ao usuário
    - Nunca explique nada
    - Sempre use function calling

    Escolha o agente correto baseado na intenção do usuário.
    """,
    tools=[
        {
            "function_declarations": [
                {
                    "name": "duvidas",
                    "description": "Encaminha para agente de dúvidas"
                },
                {
                    "name": "orcamento",
                    "description": "Encaminha para agente de orçamento"
                },
                {
                    "name": "agendamento",
                    "description": "Encaminha para agente de agendamento"
                }
            ]
        }
    ],
    tool_config={
        "function_calling_config": {
            "mode": "ANY"
        }
    },
    generation_config={
        "temperature": 0.0
    }
)