from BaseAgente import BaseAgente
from services.rag_service import buscar_contexto_sobre

class AgenteDuvidas(BaseAgente):
    def __init__(self):
        super().__init__("""
                         Você é um especialista de suporte técnico.
                         Sua função é responder dúvidas de forma clara e simples.
                         Regras:
                         - Explicar serviços e processos
                         - Explicar a empresa
                         - Não falar de preço (a menos que perguntado)
                         - Não agendar
                         """)
        
    def responder(self, msg: str):
        contexto = buscar_contexto_sobre(msg)
        prompt = self._montar_prompt(msg, contexto)
        return super().responder(prompt)

    def _montar_prompt(self, msg: str, contexto: str):

        if contexto:
            return f"""
            Você é um assistente da Powerseg
            Use o contexto abaixo para responder com precisão.
            Contexto da empresa:{contexto}
            Pergunta do cliente:{msg}"""
            
        return f"""Você é um assistente da Powerseg.Responda com base no seu conhecimento interno e boas práticas.Pergunta do cliente:{msg}"""