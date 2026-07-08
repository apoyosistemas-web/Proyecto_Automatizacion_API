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

        # Mensaje
        message_id = datos.get("id")
        mensaje = (datos.get("content") or "").strip()

        print(f"Evento          : {evento}")
        print(f"Conversation ID : {conversation_id}")
        print(f"Message ID      : {message_id}")
        print(f"Contact ID      : {contact_id}")
        print(f"Nombre          : {nombre}")
        print(f"Teléfono        : {telefono}")
        print(f"Mensaje         : {mensaje}")

        # Validar si el mensaje corresponde a un módulo
        if self.motor.existe_modulo(mensaje):

            print("\nMódulo encontrado.")

        else:

            print("\nEl mensaje no corresponde a ningún módulo.")

        print("=" * 60)