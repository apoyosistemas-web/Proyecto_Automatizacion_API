class Messages:

    @staticmethod
    def confirmacion(datos):

        return f"""
✅ Hemos recibido tu solicitud.

📂 Módulo:
{datos["modulo"]}

📄 Caso:
{datos["caso"]}

🎯 Prioridad:
{datos["prioridad"].upper()}

👤 Nivel de atención:
{datos["nivel"]}

En unos momentos uno de nuestros asesores continuará la atención.

Gracias por comunicarte con nosotros.
"""

    @staticmethod
    def error_opcion():

        return (
            "❌ La opción seleccionada no existe.\n\n"
            "Por favor selecciona una opción válida."
        )

    @staticmethod
    def error_modulo():

        return (
            "❌ No encontramos ese módulo.\n\n"
            "Por favor escribe uno de los módulos disponibles."
        )

    @staticmethod
    def despedida():

        return (
            "Gracias por comunicarte con Fomentamos.\n"
            "Que tengas un excelente día."
        )