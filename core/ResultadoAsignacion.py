#Constructor de la Clase ResultadosAsignacion:

class ResultadoAsignacion:
    def __init__(self, asignaciones, valor_objetivo):
        if asignaciones is None:
            raise ValueError("La lista de asignaciones no puede ser nula.")
        self.asignaciones = asignaciones
        self.valor_objetivo = valor_objetivo

    def mostrar_resultado(self):
        print("==== Resultado de la Asignación ====")
        print(f"Valor objetivo: {self.valor_objetivo}")
        for asignacion in self.asignaciones:
            print(asignacion)
    
    def __str__(self):
        return f"ResultadoAsignacion(valor_objetivo={self.valor_objetivo}, asignaciones={self.asignaciones})"