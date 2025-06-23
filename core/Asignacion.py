from core.Aula import Aula
from core.Grupo import Grupo
from core.Horario import Horario

# === Clase Asignacion ===
class Asignacion:
    #Constructor de la Clase Asignacion: Representa la asignación de un grupo a un aula en un horario
    def __init__(self, grupo: 'Grupo', aula: 'Aula', horario: 'Horario'):
        if grupo is None or aula is None or horario is None:
            raise ValueError("Grupo, Aula y Horario no pueden ser nulos.")

        self._grupo = grupo
        self._aula = aula
        self._horario = horario
    
    @property
    def grupo(self)->'Grupo':
        return self._grupo

    @property
    def aula(self)->'Aula':
        return self._aula

    @property
    def horario(self)->'Horario':
        return self._horario


    def __str__(self):
        return (f"Asignacion(grupo={self.grupo.id_grupo} ({self.grupo.materia}), "
                f"aula={self.aula.id_aula} (Capacidad: {self.aula.capacidad}), "
                f"horario={self.horario.id_horario} ({self.horario.bloque}))")