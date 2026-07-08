class RulesEngine:

    def __init__(self, dataframe):
        self.df = dataframe

    def buscar_modulo(self, modulo):
        """
        Retorna todos los casos pertenecientes a un módulo.
        """
        resultado = self.df[
            self.df["Módulo"].str.upper() == modulo.upper()
        ]

        return resultado

    def existe_modulo(self, modulo):
        """
        Verifica si el módulo existe en el Excel.
        """
        resultado = self.buscar_modulo(modulo)

        return not resultado.empty

    def buscar_codigo(self, codigo):
        """
        Busca un código específico y retorna toda la fila.
        """
        resultado = self.df[
            self.df["Codigo"].str.upper() == codigo.upper()
        ]

        if resultado.empty:
            return None

        return resultado.iloc[0]