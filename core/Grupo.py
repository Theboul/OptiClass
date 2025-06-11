
class Grupo:
    #Constructor de la Clase Grupo:
    def __init__(self, id_grupo: int, cantidad_estudiantes: int, materia: str):
        if not isinstance(id_grupo, int) or id_grupo <= 0:
            raise ValueError("ID del grupo debe ser un entero positivo.")
        
        if not isinstance(cantidad_estudiantes, int) or cantidad_estudiantes <= 0:
            raise ValueError("Cantidad de estudiantes debe ser un entero positivo.")
        
        if not materia or not materia.strip():
            raise ValueError("Materia no puede ser nula o vacía.")

        self._id_grupo = id_grupo
        self._cantidad_estudiantes = cantidad_estudiantes
        self._materia = materia
    
    @property
    def id_grupo(self) -> int:
        return self._id_grupo

    @property
    def cantidad_estudiantes(self) -> int:
        return self._cantidad_estudiantes

    @property
    def materia(self) -> str:
        return self._materia

    def __str__(self):
        return f"Grupo(id={self.id_grupo}, cantidad_estudiantes={self.cantidad_estudiantes}, materia='{self.materia}')"
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Grupo':
        return cls(
            id_grupo=data['id_grupo'],
            cantidad_estudiantes=data['cantidad_estudiantes'],
            materia=data['materia']
        )
    
    def to_dict(self):
        return {
            "id_grupo": self.id_grupo,
            "cantidad_estudiantes": self.cantidad_estudiantes,
            "materia": self.materia
        }
