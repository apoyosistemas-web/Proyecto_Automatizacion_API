import requests

from config.settings import (
    CHATWOOT_URL,
    CHATWOOT_API_TOKEN,
    CHATWOOT_ACCOUNT_ID,
)


class Chatwoot:
    def __init__(self):
        self.base_url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}"

        self.headers = {
            "api_access_token": CHATWOOT_API_TOKEN,
            "Content-Type": "application/json"
        }

    def obtener_agentes(self):
        url = f"{self.base_url}/agents"

        respuesta = requests.get(
            url=url,
            headers=self.headers
        )

        return respuesta

    def obtener_equipos(self):
        url = f"{self.base_url}/teams"

        respuesta = requests.get(
            url=url,
            headers=self.headers
        )

        return respuesta

    def obtener_etiquetas(self):
        url = f"{self.base_url}/labels"

        respuesta = requests.get(
            url=url,
            headers=self.headers
        )

        return respuesta

