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
    
    def construir_menu(self, modulo):

        casos = self.buscar_modulo(modulo)

        if casos.empty:
            return None

        mensaje = []
        mensaje.append(f"Módulo: {modulo}")
        mensaje.append("")
        mensaje.append("Seleccione el caso que presenta:")
        mensaje.append("")

        for _, fila in casos.iterrows():
            mensaje.append(f"{fila['Codigo']} - {fila['Caso']}")

        mensaje.append("")
        mensaje.append("Escriba únicamente el código.")

        return "\n".join(mensaje)
    
    def buscar_opcion(self, modulo, opcion):

        casos = self.buscar_modulo(modulo)

        if casos.empty:
            return None

        try:
            indice = int(opcion) - 1
        except ValueError:
            return None

        if indice < 0 or indice >= len(casos):
            return None

        return casos.iloc[indice]