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

    # =====================================================
    # CONSULTAS
    # =====================================================

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

    # =====================================================
    # ACTUALIZAR CONVERSACIÓN
    # =====================================================

    def actualizar_conversacion(
        self,
        conversation_id,
        team_id,
        agente_id,
        prioridad
    ):

        url = (
            f"{CHATWOOT_URL}/api/v1/accounts/"
            f"{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}"
        )

        payload = {
            "team_id": int(team_id),
            "assignee_id": int(agente_id),
            "priority": prioridad
        }

        try:

            respuesta = requests.patch(
                url,
                json=payload,
                headers=self.headers
            )

            return {
                "ok": respuesta.status_code == 200,
                "status": respuesta.status_code,
                "response": respuesta
            }

        except Exception as e:

            return {
                "ok": False,
                "status": 500,
                "error": str(e)
            }

    # =====================================================
    # AGREGAR ETIQUETA
    # =====================================================

    def agregar_etiqueta(self, conversation_id, etiqueta):

        url = (
            f"{CHATWOOT_URL}/api/v1/accounts/"
            f"{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}/labels"
        )

        payload = {
            "labels": [
                etiqueta
            ]
        }

        try:

            respuesta = requests.post(
                url,
                json=payload,
                headers=self.headers
            )

            return {
                "ok": respuesta.status_code in [200, 201],
                "status": respuesta.status_code,
                "response": respuesta
            }

        except Exception as e:

            return {
                "ok": False,
                "status": 500,
                "error": str(e)
            }

    # =====================================================
    # ENVIAR MENSAJE
    # =====================================================

    def enviar_mensaje(self, conversation_id, mensaje):

        url = (
            f"{CHATWOOT_URL}/api/v1/accounts/"
            f"{CHATWOOT_ACCOUNT_ID}/conversations/"
            f"{conversation_id}/messages"
        )

        payload = {
            "content": mensaje,
            "message_type": "outgoing"
        }

        try:

            respuesta = requests.post(
                url,
                json=payload,
                headers=self.headers
            )

            return {
                "ok": respuesta.status_code in [200, 201],
                "status": respuesta.status_code,
                "response": respuesta
            }

        except Exception as e:

            return {
                "ok": False,
                "status": 500,
                "error": str(e)
            }

    # =====================================================
    # MÉTODOS TEMPORALES
    # =====================================================

    def asignar_equipo(self, conversation_id, team_id):

        url = (
            f"{CHATWOOT_URL}/api/v1/accounts/"
            f"{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}"
        )

        payload = {
            "team_id": int(team_id)
        }

        return requests.patch(
            url,
            json=payload,
            headers=self.headers
        )

    def asignar_agente(self, conversation_id, agente_id):

        url = (
            f"{CHATWOOT_URL}/api/v1/accounts/"
            f"{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}"
        )

        payload = {
            "assignee_id": int(agente_id)
        }

        return requests.patch(
            url,
            json=payload,
            headers=self.headers
        )