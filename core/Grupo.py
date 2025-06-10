#Constructor de la Clase Grupo:

class Grupo:
    def __init__(self, id_grupo, cantidad_estudiantes, materia):
        if id_grupo <= 0:
            raise ValueError("ID del grupo debe ser positivo.")
        if cantidad_estudiantes <= 0:
            raise ValueError("Cantidad de estudiantes debe ser positiva.")
        if not materia or materia.strip() == "":
            raise ValueError("Materia no puede ser nula o vacía.")

        self.id_grupo = id_grupo
        self.cantidad_estudiantes = cantidad_estudiantes
        self.materia = materia

    def __str__(self):
        return f"Grupo(id={self.id_grupo}, cantidad_estudiantes={self.cantidad_estudiantes}, materia='{self.materia}')"