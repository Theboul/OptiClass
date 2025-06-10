#Constructor de la Clase Horario:

class Horario:
    def __init__(self, id_horario, bloque):
        if id_horario <= 0:
            raise ValueError("ID del horario debe ser positivo.")
        if not bloque or bloque.strip() == "":
            raise ValueError("Bloque horario no puede ser nulo o vacío.")

        self.id_horario = id_horario
        self.bloque = bloque

    def __str__(self):
        return f"Horario(id={self.id_horario}, bloque='{self.bloque}')"