from BaseAgente import BaseAgente
from services.rag_service import buscar_contexto_orcamento


class AgenteOrcamento(BaseAgente):
    def __init__(self):
        super().__init__("""
                         Você é um consultor comercial.
                         Sua função é entender a necessidade do cliente e gerar orçamento.
                         Regras:
                         - Coletar informações (tipo de serviço, local, urgência)
                         - Ser objetivo e comercial
                         - Nunca agendar serviço
                         - Nunca encaminhar para outros agentes
                         """)
        
    def responder(self, msg: str):
        contexto = buscar_contexto_orcamento(msg)
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