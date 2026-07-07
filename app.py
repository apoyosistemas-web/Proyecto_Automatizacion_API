from flask import Flask, request, jsonify

from modules.webhook import WebhookHandler

app = Flask(__name__)

webhook = WebhookHandler()


@app.route("/", methods=["GET"])
def inicio():
    return "Servidor de automatización Chatwoot funcionando."


@app.route("/webhook", methods=["POST"])
def recibir_webhook():

    datos = request.json

    webhook.procesar(datos)

    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)