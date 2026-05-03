import os
import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from services.chat_service import processar_chat

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class PromptRequest(BaseModel):
    prompt: str
    cliente_id: str = "usuario_unico"

app.mount("/front", StaticFiles(directory="front"), name="front")

@app.get("/")
def ler_index_front():
    return FileResponse("front/index.html")

@app.post("/chat")
def chat(req: PromptRequest):
    resposta = processar_chat(req.prompt, req.cliente_id)
    return {"resposta": resposta}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)