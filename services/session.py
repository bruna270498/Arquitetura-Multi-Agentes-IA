from datetime import datetime, timedelta
import threading
import time

sessoes = {}

# Atualiza interação
def atualizar_interacao(cliente_id):
    if cliente_id not in sessoes:
        sessoes[cliente_id] = {}

    sessoes[cliente_id]["ultima_interacao"] = datetime.now()
    sessoes[cliente_id]["avisado_5min"] = False
    sessoes[cliente_id]["ativa"] = True


# Saudação controlada
def ja_saudou(cliente_id):
    return sessoes.get(cliente_id, {}).get("saudou", False)


def marcar_saudacao(cliente_id):
    if cliente_id not in sessoes:
        sessoes[cliente_id] = {}

    sessoes[cliente_id]["saudou"] = True


# Envio de mensagem (placeholder)
def enviar_mensagem(cliente_id, mensagem):
    print(f"[ENVIO] {cliente_id}: {mensagem}")


# Monitor de inatividade
def monitorar_inatividade():
    while True:
        for cliente_id, dados in sessoes.items():

            ultima = dados.get("ultima_interacao")
            if not ultima:
                continue

            tempo = datetime.now() - ultima

            # ⏱️ 5 min → aviso
            if tempo > timedelta(minutes=5) and not dados.get("avisado_5min"):
                enviar_mensagem(
                    cliente_id,
                    "Você ainda está aí? Posso te ajudar em algo mais 😊"
                )
                dados["avisado_5min"] = True

            # ⏱️ 10 min → encerramento
            if tempo > timedelta(minutes=10) and dados.get("ativa"):
                enviar_mensagem(
                    cliente_id,
                    "Atendimento encerrado por inatividade. Quando precisar, é só me chamar 👍"
                )
                dados["ativa"] = False

        time.sleep(30)


# Inicia thread automaticamente
threading.Thread(target=monitorar_inatividade, daemon=True).start()