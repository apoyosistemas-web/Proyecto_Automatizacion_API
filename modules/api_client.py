from modules.round_robin import RoundRobin


class ApiClient:

    def __init__(self):

        self.round_robin = RoundRobin()

    def preparar_datos(self, conversation_id, contact_id, caso):

        agentes = []

        if caso["Agente_ID"]:

            agentes = [
                agente.strip()
                for agente in str(caso["Agente_ID"]).split(",")
            ]

        # Seleccionar automáticamente el agente
        agente_seleccionado = self.round_robin.siguiente_agente(agentes)

        datos = {

            "conversation_id": conversation_id,
            "contact_id": contact_id,

            "codigo": caso["Codigo"],
            "modulo": caso["Módulo"],
            "caso": caso["Caso"],

            "equipo_id": caso["Equipo_ID"],
            "equipo": caso["Equipo"],

            "agentes_disponibles": agentes,
            "agente_seleccionado": agente_seleccionado,

            "prioridad": caso["Prioridad"],
            "etiqueta": caso["Etiqueta"],
            "nivel": caso["Nivel de atención"]

        }

        return datos