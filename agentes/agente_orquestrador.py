import os
from google import genai
from google.genai import types

#Vertex Empresarial!
client = genai.Client(
    vertexai=True,
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION")
)

MODEL = os.getenv("MODEL_ID")

SYSTEM = """
Você é um roteador de atendimento.
Sua única função é escolher qual agente deve atender o usuário.

Agentes disponíveis:
- duvidas: informações, quais serviços fazemos, como funciona.
- orcamento: cliente quer saber preço, valor, quanto custa, ou simular orçamento.
- agendamento: cliente quer agendar visita técnica ou confirmar.

Responda APENAS com uma palavra: duvidas, orcamento ou agendamento.
"""

def extrair_agente(mensagem: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=mensagem,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM,
                temperature=0.0
            )
        )
        
        # Pega o texto com segurança para não dar o erro de 'NoneType'
        texto = response.text if response.text else ""
        agente = texto.strip().lower()
        
        print(f"🕵️ ORQUESTRADOR ESCOLHEU: '{agente}'")
        
        # Procura a palavra mágica dentro da resposta
        if "orcamento" in agente:
            return "orcamento"
        elif "agendamento" in agente:
            return "agendamento"
        else:
            return "duvidas"
            
    except Exception as e:
        print(f"Erro no Orquestrador: {e}")       
    return "duvidas"