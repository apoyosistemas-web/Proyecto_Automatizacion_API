from modules.logger import Logger


def test_logger():

    logger = Logger()

    logger.info("Proyecto iniciado")
    logger.info("Prueba del sistema de logs")
    logger.warning("Este es un mensaje de advertencia")
    logger.error("Este es un mensaje de error")


if __name__ == "__main__":
    test_logger()