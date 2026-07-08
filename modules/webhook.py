from modules.api_client import ApiClient

# Memoria temporal
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

        # -------------------------------------------------

        if self.motor.existe_modulo(mensaje):

            conversaciones[conversation_id] = {
                "modulo": mensaje
            }

            menu = self.motor.construir_menu(mensaje)

            print()
            print(menu)

            return

        # -------------------------------------------------

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

                for clave, valor in datos_chatwoot.items():

                    print(f"{clave:18}: {valor}")

                print("=" * 60)

                return

        print()

        print("No se encontró el módulo ni una opción válida.")