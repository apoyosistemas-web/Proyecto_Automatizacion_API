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
                # ASIGNAR EQUIPO
                # =====================================================

                print()
                print("=" * 60)
                print("ASIGNANDO EQUIPO EN CHATWOOT")
                print("=" * 60)

                try:

                    respuesta_equipo = self.chatwoot.asignar_equipo(
                        conversation_id=datos_chatwoot["conversation_id"],
                        team_id=datos_chatwoot["equipo_id"]
                    )

                    print(f"HTTP Status : {respuesta_equipo.status_code}")

                    if respuesta_equipo.status_code == 200:

                        print("✅ Equipo asignado correctamente.")

                        # ===============================================
                        # ASIGNAR AGENTE
                        # ===============================================

                        print()
                        print("=" * 60)
                        print("ASIGNANDO AGENTE EN CHATWOOT")
                        print("=" * 60)

                        respuesta_agente = self.chatwoot.asignar_agente(
                            conversation_id=datos_chatwoot["conversation_id"],
                            agente_id=datos_chatwoot["agente_seleccionado"]
                        )

                        print(
                            f"Agente seleccionado : "
                            f"{datos_chatwoot['agente_seleccionado']}"
                        )

                        print(
                            f"HTTP Status         : "
                            f"{respuesta_agente.status_code}"
                        )

                        if respuesta_agente.status_code == 200:

                            print("✅ Agente asignado correctamente.")

                        else:

                            print("❌ Error al asignar el agente.")
                            print(respuesta_agente.text)

                    else:

                        print("❌ Error al asignar el equipo.")
                        print(respuesta_equipo.text)

                except Exception as e:

                    print("❌ Error de conexión con Chatwoot.")
                    print(e)

                print("=" * 60)

                return

        print()
        print("No se encontró el módulo ni una opción válida.")