#Implementa el sistema de auditoría del proyecto.

import logging
from pathlib import Path


class Logger:

    def __init__(self):

        log_folder = Path("logs")
        log_folder.mkdir(exist_ok=True)

        self.logger = logging.getLogger("ChatwootAutomation")

        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:

            archivo = logging.FileHandler(
                log_folder / "automatizacion.log",
                encoding="utf-8"
            )

            formato = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            archivo.setFormatter(formato)

            self.logger.addHandler(archivo)

    def info(self, mensaje):

        self.logger.info(mensaje)

    def error(self, mensaje):

        self.logger.error(mensaje)

    def warning(self, mensaje):

        self.logger.warning(mensaje)