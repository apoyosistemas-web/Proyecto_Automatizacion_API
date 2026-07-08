from flask import Flask, request, jsonify

from modules.webhook import WebhookHandler
from modules.reader import ExcelReader
from modules.rules import RulesEngine

app = Flask(__name__)

# Cargar Excel una sola vez
excel = ExcelReader("data/casos.xlsx")
casos = excel.load_cases()

# Crear el motor de reglas
motor = RulesEngine(casos)

# Crear el webhook con el motor
webhook = WebhookHandler(motor)

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