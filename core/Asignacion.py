
class Asignacion:
    def __init__(self, grupo, aula, horario):
        if grupo is None or aula is None or horario is None:
            raise ValueError("Grupo, Aula y Horario no pueden ser nulos.")

        self.grupo = grupo
        self.aula = aula
        self.horario = horario

    def __str__(self):
        return (f"Asignacion(grupo={self.grupo.id_grupo} ({self.grupo.materia}), "
                f"aula={self.aula.id_aula} (Capacidad: {self.aula.capacidad}), "
                f"horario={self.horario.id_horario} ({self.horario.bloque}))")