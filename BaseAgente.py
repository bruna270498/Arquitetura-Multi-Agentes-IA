from vertexai.generative_models import GenerativeModel, GenerationConfig
from regra_global import REGRA_GLOBAL


class BaseAgente:
    def __init__(self, funcao):
        self.model = GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=REGRA_GLOBAL + funcao,
            generation_config={
                "temperature": 0.5
            }
        )
    def responder(self, mensagem):
        response = self.model.generate_content(mensagem)
        return response.text