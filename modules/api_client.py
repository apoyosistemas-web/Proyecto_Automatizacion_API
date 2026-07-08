class ApiClient:

    def preparar_datos(self, conversation_id, contact_id, caso):

        agentes = []

        if caso["Agente_ID"]:

            agentes = [
                agente.strip()
                for agente in str(caso["Agente_ID"]).split(",")
            ]

        datos = {

            "conversation_id": conversation_id,
            "contact_id": contact_id,

            "codigo": caso["Codigo"],
            "modulo": caso["Módulo"],
            "caso": caso["Caso"],

            "equipo_id": caso["Equipo_ID"],
            "equipo": caso["Equipo"],

            "agentes": agentes,

            "prioridad": caso["Prioridad"],
            "etiqueta": caso["Etiqueta"],
            "nivel": caso["Nivel de atención"]

        }

        return datos