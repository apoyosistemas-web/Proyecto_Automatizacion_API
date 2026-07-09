from modules.api_client import ApiClient
from modules.chatwoot import Chatwoot

# Memoria temporal de conversaciones
conversaciones = {}


class WebhookHandler:

    def __init__(self, motor):

        self.motor = motor
        self.api = ApiClient()
        self.chatwoot = Chatwoot()

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
        # EL USUARIO ESCRIBIÓ UN MÓDULO
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
        # EL USUARIO ESCOGIÓ UNA OPCIÓN
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
                print("DATOS PREPARADOS")
                print("=" * 60)

                for clave, valor in datos_chatwoot.items():
                    print(f"{clave:22}: {valor}")

                print("=" * 60)

                # =====================================================
                # ACTUALIZAR CONVERSACIÓN
                # =====================================================

                print()
                print("=" * 60)
                print("ACTUALIZANDO CONVERSACIÓN")
                print("=" * 60)

                resultado = self.chatwoot.actualizar_conversacion(
                    conversation_id=datos_chatwoot["conversation_id"],
                    team_id=datos_chatwoot["equipo_id"],
                    agente_id=datos_chatwoot["agente_seleccionado"],
                    prioridad=datos_chatwoot["prioridad"]
                )

                if resultado["ok"]:

                    print("✅ Conversación actualizada correctamente")

                else:

                    print("❌ No fue posible actualizar la conversación")
                    print(f"HTTP: {resultado['status']}")

                    if "response" in resultado:
                        print(resultado["response"].text)

                # =====================================================
                # AGREGAR ETIQUETA
                # =====================================================

                print()
                print("=" * 60)
                print("AGREGANDO ETIQUETA")
                print("=" * 60)

                etiqueta = self.chatwoot.agregar_etiqueta(
                    conversation_id=datos_chatwoot["conversation_id"],
                    etiqueta=datos_chatwoot["etiqueta"]
                )

                if etiqueta["ok"]:

                    print("✅ Etiqueta agregada correctamente")
                    print(f"Etiqueta: {datos_chatwoot['etiqueta']}")

                else:

                    print("❌ Error agregando la etiqueta")
                    print(f"HTTP: {etiqueta['status']}")

                    if "response" in etiqueta:
                        print(etiqueta["response"].text)

                print("=" * 60)

                return

        print()
        print("No se encontró el módulo ni una opción válida.")