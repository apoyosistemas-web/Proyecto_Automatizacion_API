# Automatización Inteligente para Chatwoot

## Descripción

Este proyecto implementa una automatización desarrollada en Python para integrarse con Chatwoot mediante Webhooks y su API REST.

El objetivo es automatizar la clasificación de solicitudes recibidas por WhatsApp, identificar el módulo solicitado por el usuario, mostrar dinámicamente los casos disponibles, asignar automáticamente el equipo, el agente, la prioridad y las etiquetas correspondientes, reduciendo significativamente el trabajo manual del área de soporte.

---

# Objetivos

- Automatizar la atención inicial de los usuarios.
- Reducir tiempos de clasificación de tickets.
- Asignar automáticamente conversaciones.
- Distribuir carga entre agentes mediante Round Robin.
- Centralizar la configuración de casos utilizando Excel.
- Facilitar futuras integraciones con Inteligencia Artificial.

---

# Tecnologías utilizadas

- Python 3
- Flask
- Pandas
- OpenPyXL
- Requests
- Python-dotenv
- Chatwoot API
- Webhooks
- Ngrok
- Git
- GitHub
- Visual Studio Code

---

# Arquitectura del proyecto

Usuario

↓

WhatsApp

↓

Meta Cloud API

↓

Chatwoot

↓

Webhook

↓

Flask

↓

Rules Engine

↓

Excel

↓

Round Robin

↓

API Chatwoot

↓

Asignación automática

↓

Equipo

↓

Agente

↓

Prioridad

↓

Etiqueta

↓

Respuesta automática

---

# Flujo de funcionamiento

1. El usuario escribe por WhatsApp.

2. Chatwoot recibe el mensaje.

3. Chatwoot envía un Webhook.

4. Flask recibe el evento.

5. Se valida el tipo de evento.

6. Se identifica el módulo solicitado.

7. Se genera automáticamente el menú de opciones.

8. El usuario selecciona el caso.

9. Se consultan los datos del Excel.

10. Se ejecuta Round Robin.

11. Se prepara la información.

12. Se actualiza la conversación mediante la API de Chatwoot.

13. Se asigna:

- Equipo
- Agente
- Prioridad
- Etiqueta

14. Se envía un mensaje de confirmación al usuario.

15. Se registra toda la operación en el sistema de Logs.

---

# Estructura del proyecto

```text
Proyecto_Automatizacion_API/

app.py
main.py
requirements.txt
README.md

config/
settings.py

data/
casos.xlsx
round_robin.json

logs/
automatizacion.log

modules/
api_client.py
chatwoot.py
logger.py
messages.py
reader.py
round_robin.py
rules.py
session_manager.py
webhook.py

tests/

.env
```

---

# Variables de entorno

Crear un archivo `.env`

```env
CHATWOOT_URL=

CHATWOOT_API_TOKEN=

CHATWOOT_ACCOUNT_ID=
```

---

# Instalación

Crear entorno virtual

```bash
python -m venv .venv
```

Activar entorno

Windows

```bash
.venv\Scripts\activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecutar el proyecto

```bash
python main.py
```

---

# Funcionalidades implementadas

- Recepción de Webhooks
- Identificación automática de módulos
- Generación dinámica del menú
- Lectura de Excel
- Motor de reglas
- Selección automática del caso
- Distribución Round Robin
- Integración con Chatwoot
- Asignación de equipos
- Asignación de agentes
- Asignación de prioridad
- Asignación de etiquetas
- Envío de mensajes automáticos
- Gestión de sesiones
- Sistema de Logs

---

# Estado del proyecto

Actualmente el proyecto se encuentra en fase de pruebas de integración con Chatwoot y WhatsApp.

Toda la lógica de negocio ya se encuentra implementada.

---

# Mejoras futuras

- Integración con Inteligencia Artificial.
- Base de datos PostgreSQL.
- Panel de administración.
- Configuración web de módulos.
- Estadísticas en Power BI.
- Dashboard administrativo.
- Integración con Microsoft Teams.
- Integración con Power Automate.
- Automatización de respuestas mediante IA.

---

# Autor

Proyecto desarrollado por:

**Elsy Mariana Pérez Montalvo**

Proyecto desarrollado durante las prácticas profesionales en Fomentamos.