import json
from pathlib import Path


class RoundRobin:

    def __init__(self):

        self.file = Path("data/round_robin.json")

        if not self.file.exists():

            self.file.write_text("{}")

    def siguiente_agente(self, agentes):

        # Si solo existe un agente, no hay balanceo
        if len(agentes) == 1:
            return agentes[0]

        # Leer historial
        datos = json.loads(self.file.read_text())

        # La llave será el grupo de agentes
        clave = ",".join(agentes)

        ultimo = datos.get(clave, -1)

        siguiente = (ultimo + 1) % len(agentes)

        datos[clave] = siguiente

        self.file.write_text(
            json.dumps(
                datos,
                indent=4
            )
        )

        return agentes[siguiente]