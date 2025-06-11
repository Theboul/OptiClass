from core.Aula import Aula
from core.Grupo import Grupo
from core.Horario import Horario
from typing import List

class Parametros:
    #Constructor de la Clase Parametros:
    def __init__(self, delta: float, lambda_penalizacion: float, 
                 aulas: List['Aula'], grupos: List['Grupo'], horarios: List['Horario']):
        if not (0 <= delta <= 1):
            raise ValueError("Umbral (delta) debe estar entre 0 y 1.")
        
        if lambda_penalizacion < 0:
            raise ValueError("Penalización (lambda) no puede ser negativa.")
        
        if not aulas or not all(isinstance(a, Aula) for a in aulas):
            raise ValueError("Debe haber al menos un aula válida.")
        
        if not grupos or not all(isinstance(g, Grupo) for g in grupos):
            raise ValueError("Debe haber al menos un grupo válido.")
        
        if not horarios or not all(isinstance(h, Horario) for h in horarios):
            raise ValueError("Debe haber al menos un horario válido.")

        self._delta = delta
        self._lambda_penalizacion = lambda_penalizacion
        self._aulas = aulas
        self._grupos = grupos
        self._horarios = horarios

    @property
    def delta(self) -> float:
        return self._delta

    @property
    def lambda_penalizacion(self) -> float:
        return self._lambda_penalizacion

    @property
    def aulas(self) -> List['Aula']:
        return self._aulas.copy()

    @property
    def grupos(self) -> List['Grupo']:
        return self._grupos.copy()

    @property
    def horarios(self) -> List['Horario']:
        return self._horarios.copy()
    
    def __str__(self):
        return (f"Parametros(delta={self.delta}, lambda={self.lambda_penalizacion}, "
                f"aulas={self.aulas}, grupos={self.grupos}, horarios={self.horarios})")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Parametros':
        aulas = [Aula.from_dict(a) for a in data['aulas']]
        grupos = [Grupo.from_dict(g) for g in data['grupos']]
        horarios = [Horario.from_dict(h) for h in data['horarios']]
        return cls(
            delta=data['delta'],
            lambda_penalizacion=data['lambda_penalizacion'],
            aulas=aulas,
            grupos=grupos,
            horarios=horarios
        )

    def to_dict(self):
        return {
            "delta": self.delta,
            "lambda_penalizacion": self.lambda_penalizacion,
            "aulas": [a.to_dict() for a in self.aulas],
            "grupos": [g.to_dict() for g in self.grupos],
            "horarios": [h.to_dict() for h in self.horarios]
        }
