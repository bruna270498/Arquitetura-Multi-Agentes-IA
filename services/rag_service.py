from vertexai.language_models import TextEmbeddingModel
from google.cloud import datastore
import math

ds_client = datastore.Client()

model = TextEmbeddingModel.from_pretrained("textembedding-gecko")


def gerar_embedding(texto):
    return model.get_embeddings([texto])[0].values


def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(x*x for x in b))
    return dot / (norm_a * norm_b)


def buscar_contexto(pergunta, categoria=None):
    emb_pergunta = gerar_embedding(pergunta)

    query = ds_client.query(kind="powerseg_knowledge")

    if categoria:
        query.add_filter("category", "=", categoria)

    dados = list(query.fetch())

    resultados = []

    for item in dados:
        emb = item.get("embedding")
        if not emb:
            continue

        score = cosine_similarity(emb_pergunta, emb)

        resultados.append({
            "score": score,
            "content": item["content"]
        })

    resultados.sort(key=lambda x: x["score"], reverse=True)

    top = resultados[:3]

    return "\n".join([r["content"] for r in top])