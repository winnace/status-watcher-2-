from flask import Flask, request, jsonify
import requests
import time
import threading

app = Flask(__name__)

# Configurações (trocar pelos seus valores)
SERVER_IP = "IP_DO_SEU_SERVIDOR"
SERVER_PORT = "30120"
BOTGHOST_WEBHOOK_URL = "https://api.botghost.com/webhooks/SEU_WEBHOOK_AQUI"

online_ja_notificado = False

def verifica_servidor():
    global online_ja_notificado
    while True:
        try:
            url = f"http://{SERVER_IP}:{SERVER_PORT}/players.json"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                if not online_ja_notificado:
                    print("Servidor FiveM está ONLINE!")
                    # Envia pro BotGhost
                    requests.post(BOTGHOST_WEBHOOK_URL, json={"status": "online"})
                    online_ja_notificado = True
            else:
                print("Servidor pode estar offline ou respondeu com código:", resp.status_code)
                online_ja_notificado = False
        except Exception as e:
            print("Erro ao checar servidor:", e)
            online_ja_notificado = False

        time.sleep(60)  # verifica a cada 60 segundos

# Rota pro webhook ou pra ver se está vivo
@app.route('/')
def index():
    return "OK", 200

if __name__ == '__main__':
    # Inicia thread pra checagem
    thread = threading.Thread(target=verifica_servidor, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
