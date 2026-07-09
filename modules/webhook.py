from modules.api_client import ApiClient
from modules.chatwoot import Chatwoot
from modules.messages import Messages
from modules.session_manager import SessionManager



class WebhookHandler:

    def __init__(self, motor):

        self.motor = motor
        self.api = ApiClient()
        self.chatwoot = Chatwoot()
        self.session = SessionManager()

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

            self.session.guardar_modulo(
                conversation_id, 
                mensaje
            )

            menu = self.motor.construir_menu(mensaje)

            print()
            print("=" * 60)
            print("MENÚ GENERADO")
            print("=" * 60)
            print(menu)
            print("=" * 60)

            print()
            print("=" * 60)
            print("ENVIANDO MENÚ A CHATWOOT")
            print("=" * 60)

            respuesta = self.chatwoot.enviar_mensaje(
                conversation_id,
                menu
            )

            if respuesta["ok"]:

                print("✅ Menú enviado correctamente.")

            else:

                print("❌ Error enviando el menú.")
                print(f"HTTP Status: {respuesta['status']}")

                if "response" in respuesta:
                    print(respuesta["response"].text)

                if "error" in respuesta:
                    print(respuesta["error"])

            print("=" * 60)

            return

        # =====================================================
        # EL USUARIO ESCOGIÓ UNA OPCIÓN
        # =====================================================

        if self.session.existe(conversation_id):

            modulo = self.session.obtener_modulo(
                conversation_id
            )

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

                    print("✅ Conversación actualizada.")

                else:

                    print("❌ Error actualizando conversación.")
                    print(f"HTTP Status: {resultado['status']}")

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

                    print("✅ Etiqueta agregada.")

                else:

                    print("❌ Error agregando etiqueta.")
                    print(f"HTTP Status: {etiqueta['status']}")

                    if "response" in etiqueta:
                        print(etiqueta["response"].text)

                
                # =====================================================
                # MENSAJE DE CONFIRMACIÓN
                # =====================================================

                mensaje_confirmacion = Messages.confirmacion(
                datos_chatwoot
                )
  
                print()
                print("=" * 60)
                print("ENVIANDO MENSAJE DE CONFIRMACIÓN")
                print("=" * 60)

                respuesta = self.chatwoot.enviar_mensaje(
                    conversation_id,
                    mensaje_confirmacion
                )

                if respuesta["ok"]:

                    print("✅ Mensaje de confirmación enviado.")

                else:

                    print("❌ Error enviando mensaje de confirmación.")
                    print(f"HTTP Status: {respuesta['status']}")

                    if "response" in respuesta:
                        print(respuesta["response"].text)

                print("=" * 60)
                
                self.session.eliminar(
                    conversation_id
                )

                return

        print()
        print("No se encontró el módulo ni una opción válida.")