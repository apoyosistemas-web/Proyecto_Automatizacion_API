# Memoria temporal de conversaciones
conversaciones = {}


class WebhookHandler:

    def __init__(self, motor):
        self.motor = motor

    def procesar(self, datos):

        print("=" * 60)
        print("WEBHOOK RECIBIDO")
        print("=" * 60)

        # Evento recibido
        evento = datos.get("event")

        # Solo procesar mensajes nuevos
        if evento != "message_created":
            print(f"Evento ignorado: {evento}")
            return

        # Conversación
        conversation_id = datos.get("conversation", {}).get("id")

        # Contacto
        contacto = datos.get("contact", {})
        contact_id = contacto.get("id")
        nombre = contacto.get("name")
        telefono = contacto.get("phone_number")

        # Mensaje recibido
        message_id = datos.get("id")
        mensaje = (datos.get("content") or "").strip()

        print(f"Evento          : {evento}")
        print(f"Conversation ID : {conversation_id}")
        print(f"Message ID      : {message_id}")
        print(f"Contact ID      : {contact_id}")
        print(f"Nombre          : {nombre}")
        print(f"Teléfono        : {telefono}")
        print(f"Mensaje         : {mensaje}")

        # ====================================================
        # PASO 1: ¿El usuario escribió un módulo?
        # ====================================================

        if self.motor.existe_modulo(mensaje):

            # Guardar el módulo seleccionado para esta conversación
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

        # ====================================================
        # PASO 2: ¿El usuario respondió una opción del menú?
        # ====================================================

        if conversation_id in conversaciones:

            modulo = conversaciones[conversation_id]["modulo"]

            caso = self.motor.buscar_opcion(modulo, mensaje)

            if caso is not None:

                print()
                print("=" * 60)
                print("CASO SELECCIONADO")
                print("=" * 60)

                print(f"Código      : {caso['Codigo']}")
                print(f"Módulo      : {caso['Módulo']}")
                print(f"Caso        : {caso['Caso']}")
                print(f"Equipo      : {caso['Equipo']}")
                print(f"Equipo ID   : {caso['Equipo_ID']}")
                print(f"Agente      : {caso['Agente']}")
                print(f"Agente ID   : {caso['Agente_ID']}")
                print(f"Prioridad   : {caso['Prioridad']}")
                print(f"Etiqueta    : {caso['Etiqueta']}")
                print(f"Nivel       : {caso['Nivel de atención']}")

                print("=" * 60)

                return

        # ====================================================
        # No se encontró ni módulo ni opción válida
        # ====================================================

        print()
        print("No se encontró el módulo ni una opción válida.")