from vertexai.generative_models import GenerativeModel
from regra_global import REGRA_GLOBAL

class BaseAgente:

    def __init__(self, system_prompt: str):
      
        self.model = GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=f"{REGRA_GLOBAL}\n\n{system_prompt}",
            generation_config={"temperature": 0.5}
        )

    def responder(self, prompt_final: str = "") -> str:
        response = self.model.generate_content(prompt_final)
        return response.text