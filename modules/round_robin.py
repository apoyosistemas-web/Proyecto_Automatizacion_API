import json
from pathlib import Path


class RoundRobin:

    def __init__(self):
        self.file = Path("data/round_robin.json")

        if not self.file.exists():
            self.file.write_text("{}")

    def siguiente_agente(self, codigo, agentes):

        datos = json.loads(self.file.read_text())

        ultimo = datos.get(codigo, -1)

        siguiente = (ultimo + 1) % len(agentes)

        datos[codigo] = siguiente

        self.file.write_text(
            json.dumps(datos, indent=4)
        )

        return agentes[siguiente]