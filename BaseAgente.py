import os
from google import genai
from google.genai import types
from regra_global import REGRA_GLOBAL

# Voltamos para o Vertex Empresarial!
client = genai.Client(
    vertexai=True,
    project="-",
    location="us-central1"
)

# No Vertex, o nome exige a versão no final. Vamos usar a mais atual e estável:
MODEL = "gemini-2.5-flash" 


class BaseAgente:
    def __init__(self, system_prompt: str):
        self.system = f"{REGRA_GLOBAL}\n\n{system_prompt}"
        self._historico = {}

    def responder(self, prompt: str, cliente_id: str = None) -> str:
        hist = self._historico.get(cliente_id, []) if cliente_id else []

        hist.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
          # ====================================================
        # INÍCIO DO RAIO-X (COLE ESTE BLOCO AQUI)
        # ====================================================
        print("\n" + "="*50)
        print("🕵️  RAIO-X: O QUE O GEMINI ESTÁ LENDO DE VERDADE?")
        print("="*50)
        print(f"📌 AGENTE ACIONADO: {self.__class__.__name__}")
        print("-" * 50)
        print("📜 SYSTEM INSTRUCTION (REGRAS):")
        print(self.system)
        print("-" * 50)
        print("📚 HISTÓRICO DA CONVERSA:")
        for h in hist:
            print(f"{h.role.upper()}: {h.parts[0].text}")
        print("="*50 + "\n")
        # ====================================================

        response = client.models.generate_content(
            model=MODEL,
            contents=hist,
            config=types.GenerateContentConfig(
                system_instruction=self.system,
                temperature=0.0,
                max_output_tokens=500
            )
        )

        resposta = response.text
        hist.append(types.Content(role="model", parts=[types.Part(text=resposta)]))

        if cliente_id:
            self._historico[cliente_id] = hist

        return resposta

    def _montar_prompt(self, msg: str, contexto: str = "") -> str:
        if contexto:
            return f"Contexto:\n{contexto}\n\nMensagem do cliente: {msg}"
        return msg