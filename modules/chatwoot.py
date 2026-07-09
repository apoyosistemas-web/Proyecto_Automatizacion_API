import requests

from config.settings import (
    CHATWOOT_URL,
    CHATWOOT_API_TOKEN,
    CHATWOOT_ACCOUNT_ID,
)


class Chatwoot:

    def __init__(self):

        self.headers = {
            "api_access_token": CHATWOOT_API_TOKEN,
            "Content-Type": "application/json"
        }

    # ==========================
    # CONSULTAS
    # ==========================

    def obtener_agentes(self):

        url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/agents"

        return requests.get(
            url,
            headers=self.headers
        )

    def obtener_equipos(self):

        url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/teams"

        return requests.get(
            url,
            headers=self.headers
        )

    def obtener_etiquetas(self):

        url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/labels"

        return requests.get(
            url,
            headers=self.headers
        )

    # ==========================
    # ACTUALIZAR CONVERSACIÓN
    # ==========================

    def asignar_equipo(self, conversation_id, team_id):

        url = (
            f"{CHATWOOT_URL}/api/v1/accounts/"
            f"{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}"
        )

        payload = {
            "team_id": int(team_id)
        }

        respuesta = requests.patch(
            url,
            json=payload,
            headers=self.headers
        )

        return respuesta