class RulesEngine:

    def __init__(self, dataframe):
        self.df = dataframe

    def buscar_modulo(self, modulo):

        resultado = self.df[
            self.df["Módulo"].str.upper() == modulo.upper()
        ]

        return resultado

    def buscar_codigo(self, codigo):

        resultado = self.df[
            self.df["Codigo"].str.upper() == codigo.upper()
        ]

        if resultado.empty:
            return None

        return resultado.iloc[0]