#Este módulo recibe y procesa los eventos enviados por Chatwoot mediante Webhooks.

from modules.api_client import ApiClient
from modules.chatwoot import Chatwoot
from modules.messages import Messages
from modules.session_manager import SessionManager
from modules.logger import Logger


class WebhookHandler:

    def __init__(self, motor):

        self.motor = motor
        self.api = ApiClient()
        self.chatwoot = Chatwoot()
        self.session = SessionManager()
        self.logger = Logger()

    def procesar(self, datos):

        print("=" * 60)
        print("WEBHOOK RECIBIDO")
        print("=" * 60)

        self.logger.info("Webhook recibido.")

        evento = datos.get("event")

        if evento != "message_created":
            print(f"Evento ignorado: {evento}")

            self.logger.warning(
                f"Evento ignorado: {evento}"
            )

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

        self.logger.info(
            f"Mensaje recibido de {nombre}: {mensaje}"
        )

        # =====================================================
        # EL USUARIO ESCRIBIÓ UN MÓDULO
        # =====================================================

        if self.motor.existe_modulo(mensaje):

            self.logger.info(
                f"Módulo seleccionado: {mensaje}"
            )

            self.session.guardar_modulo(
                conversation_id,
                mensaje
            )

            menu = self.motor.construir_menu(
                mensaje
            )

            self.logger.info(
                f"Menú generado para el módulo {mensaje}"
            )

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

                self.logger.info(
                    "Menú enviado correctamente."
                )

            else:

                print("❌ Error enviando el menú.")
                print(f"HTTP Status: {respuesta['status']}")

                self.logger.error(
                    f"Error enviando menú. HTTP {respuesta['status']}"
                )

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

            caso = self.motor.buscar_opcion(
                modulo,
                mensaje
            )

            if caso is not None:

                datos_chatwoot = self.api.preparar_datos(
                    conversation_id,
                    contact_id,
                    caso
                )

                self.logger.info(
                    f"Caso seleccionado: {datos_chatwoot['caso']}"
                )

                self.logger.info(
                    f"Agente seleccionado: {datos_chatwoot['agente_seleccionado']}"
                )

                self.logger.info(
                    f"Prioridad asignada: {datos_chatwoot['prioridad']}"
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

                    self.logger.info(
                        "Conversación actualizada correctamente."
                    )

                else:

                    print("❌ Error actualizando conversación.")
                    print(f"HTTP Status: {resultado['status']}")

                    self.logger.error(
                        f"Error actualizando conversación. HTTP {resultado['status']}"
                    )

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

                    self.logger.info(
                        f"Etiqueta agregada: {datos_chatwoot['etiqueta']}"
                    )

                else:

                    print("❌ Error agregando etiqueta.")
                    print(f"HTTP Status: {etiqueta['status']}")

                    self.logger.error(
                        f"Error agregando etiqueta. HTTP {etiqueta['status']}"
                    )

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

                    self.logger.info(
                        "Mensaje de confirmación enviado correctamente."
                    )

                else:

                    print("❌ Error enviando mensaje de confirmación.")
                    print(f"HTTP Status: {respuesta['status']}")

                    self.logger.error(
                        f"Error enviando mensaje de confirmación. HTTP {respuesta['status']}"
                    )

                    if "response" in respuesta:
                        print(respuesta["response"].text)

                print("=" * 60)

                self.session.eliminar(
                    conversation_id
                )

                self.logger.info(
                    f"Sesión finalizada para la conversación {conversation_id}"
                )

                return

        self.logger.warning(
            f"No se encontró módulo u opción válida. Mensaje: {mensaje}"
        )

        print()
        print("No se encontró el módulo ni una opción válida.")