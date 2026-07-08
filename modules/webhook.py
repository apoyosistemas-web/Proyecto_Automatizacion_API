from modules.api_client import ApiClient

# Memoria temporal de conversaciones
conversaciones = {}


class WebhookHandler:

    def __init__(self, motor):

        self.motor = motor
        self.api = ApiClient()

    def procesar(self, datos):

        print("=" * 60)
        print("WEBHOOK RECIBIDO")
        print("=" * 60)

        evento = datos.get("event")

        if evento != "message_created":
            print(f"Evento ignorado: {evento}")
            return

        conversation_id = datos.get("conversation", {}).get("id")

        contacto = datos.get("contact", {})

        contact_id = contacto.get("id")
        nombre = contacto.get("name")
        telefono = contacto.get("phone_number")

        mensaje = (datos.get("content") or "").strip()

        print(f"Nombre          : {nombre}")
        print(f"Teléfono        : {telefono}")
        print(f"Mensaje         : {mensaje}")

        # =====================================================
        # ¿El usuario escribió un módulo?
        # =====================================================

        if self.motor.existe_modulo(mensaje):

            conversaciones[conversation_id] = {
                "modulo": mensaje
            }

            menu = self.motor.construir_menu(mensaje)

            print()
            print("=" * 60)
            print("MENÚ GENERADO")
            print("=" * 60)
            print(menu)
            print("=" * 60)

            return

        # =====================================================
        # ¿El usuario respondió una opción?
        # =====================================================

        if conversation_id in conversaciones:

            modulo = conversaciones[conversation_id]["modulo"]

            caso = self.motor.buscar_opcion(modulo, mensaje)

            if caso is not None:

                datos_chatwoot = self.api.preparar_datos(
                    conversation_id,
                    contact_id,
                    caso
                )

                print()
                print("=" * 60)
                print("DATOS PREPARADOS PARA CHATWOOT")
                print("=" * 60)

                print(f"Conversation ID      : {datos_chatwoot['conversation_id']}")
                print(f"Contact ID           : {datos_chatwoot['contact_id']}")
                print(f"Código               : {datos_chatwoot['codigo']}")
                print(f"Módulo               : {datos_chatwoot['modulo']}")
                print(f"Caso                 : {datos_chatwoot['caso']}")
                print(f"Equipo               : {datos_chatwoot['equipo']}")
                print(f"Equipo ID            : {datos_chatwoot['equipo_id']}")

                print()
                print(f"Agentes disponibles  : {datos_chatwoot['agentes_disponibles']}")
                print(f"Agente seleccionado  : {datos_chatwoot['agente_seleccionado']}")

                print()
                print(f"Prioridad            : {datos_chatwoot['prioridad']}")
                print(f"Etiqueta             : {datos_chatwoot['etiqueta']}")
                print(f"Nivel                : {datos_chatwoot['nivel']}")

                print("=" * 60)

                return

        print()
        print("No se encontró el módulo ni una opción válida.")