import os
import vertexai
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from services.chat_service import processar_chat

# Config
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION')

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Request model
class PromptRequest(BaseModel):
    prompt: str
    cliente_id: str = "usuario_unico"  # depois pode vir do WhatsApp

# Front
@app.get("/")
def ler_index_front():
    return FileResponse("index.html")

# Chat
@app.post("/chat")
def chat(req: PromptRequest):
    resposta = processar_chat(req.prompt, req.cliente_id)
    return {"resposta": resposta}