#Se encarga de leer el archivo Excel que contiene la configuración
#de módulos, casos y reglas de asignación.

from pathlib import Path
import pandas as pd


class ExcelReader:
    """
    Clase encargada de leer el archivo de Excel.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load_cases(self):
        """
        Carga el archivo de Excel y retorna un DataFrame.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {self.file_path}"
            )

        dataframe = pd.read_excel(self.file_path)
        
        # Limpia los nombres de las columnas
        dataframe.columns = dataframe.columns.str.strip()

        return dataframe