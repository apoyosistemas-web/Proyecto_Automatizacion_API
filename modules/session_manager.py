#Gestiona las sesiones temporales de las conversaciones
#mientras el usuario interactúa con el bot.

class SessionManager:

    def __init__(self):

        self.conversaciones = {}

    def guardar_modulo(self, conversation_id, modulo):

        self.conversaciones[conversation_id] = {
            "modulo": modulo
        }

    def existe(self, conversation_id):

        return conversation_id in self.conversaciones

    def obtener_modulo(self, conversation_id):

        return self.conversaciones[conversation_id]["modulo"]

    def eliminar(self, conversation_id):

        if conversation_id in self.conversaciones:
            del self.conversaciones[conversation_id]

    def limpiar(self):

        self.conversaciones.clear()