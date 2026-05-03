from BaseAgente import BaseAgente
from services.session import sessoes


class AgenteAgendamento(BaseAgente):
    def __init__(self):
        super().__init__("""
Você é um assistente de agendamento da PowerSeg. Respostas curtas, 1 pergunta por vez.

Colete UMA informação por vez nesta ordem:
1. Nome completo
2. Telefone
3. Endereço completo
4. Tipo de serviço (se não vier do orçamento)
5. Urgência: normal, urgente ou emergência

Ao ter tudo, mostre o resumo:
📋 Resumo do agendamento:
👤 Nome: {nome}
📱 Telefone: {telefone}
📍 Endereço: {endereço}
🔧 Serviço: {serviço}
⚡ Urgência: {urgência}
💰 Orçamento: {valor ou 'Será avaliado na visita'}

Confirma o agendamento? ✅

REGRAS:
- 1 pergunta por vez
- Nunca faça orçamento
- Após "sim" ou "confirmo" responda: "✅ Agendado! Em breve nossa equipe entrará em contato."
""")

    def responder(self, msg: str, cliente_id: str = None) -> str:
        orcamento = ""
        if cliente_id:
            orcamento = sessoes.get(cliente_id, {}).get("orcamento", "")

        contexto = f"Orçamento aprovado:\n{orcamento}" if orcamento else ""
        prompt = self._montar_prompt(msg, contexto)
        return super().responder(prompt, cliente_id)