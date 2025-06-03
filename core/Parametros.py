
class Parametros:
    def __init__(self, delta, lambda_penalizacion, aulas, grupos, horarios):
        if delta < 0 or delta > 1:
            raise ValueError("Umbral debe estar entre 0 y 1.")
        if lambda_penalizacion < 0:
            raise ValueError("Penalización no puede ser negativa.")
        if not aulas:
            raise ValueError("Debe haber al menos un aula.")
        if not grupos:
            raise ValueError("Debe haber al menos un grupo.")
        if not horarios:
            raise ValueError("Debe haber al menos un horario.")

        self.delta = delta
        self.lambda_penalizacion = lambda_penalizacion
        self.aulas = aulas
        self.grupos = grupos
        self.horarios = horarios

    def __str__(self):
        return (f"Parametros(delta={self.delta}, lambda={self.lambda_penalizacion}, "
                f"aulas={self.aulas}, grupos={self.grupos}, horarios={self.horarios})")