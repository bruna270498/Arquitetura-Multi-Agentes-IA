import os
from vertexai.preview import rag
from dotenv import load_dotenv

load_dotenv()

RAG_SOBRE_ID = os.getenv("RAG_SOBRE_ID")
RAG_ORCAMENTO_ID = os.getenv("RAG_ORCAMENTO_ID")

def _query_rag(corpus_id: str, pergunta: str):
    """
    Função genérica para qualquer RAG
    """
    corpus = rag.RagCorpus(corpus_id)
    response = corpus.query(text=pergunta)
    return response

def buscar_contexto_sobre(pergunta: str) -> str:
    return _query_rag(RAG_SOBRE_ID, pergunta)

def buscar_contexto_orcamento(pergunta: str) -> str:
    return _query_rag(RAG_ORCAMENTO_ID, pergunta)