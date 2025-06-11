from pydantic import BaseModel, validator
from typing import List
import re

class AulaModel(BaseModel):
    id_aula: int
    capacidad: int
    piso: int

class GrupoModel(BaseModel):
    id_grupo: int
    cantidad_estudiantes: int
    materia: str

class HorarioModel(BaseModel):
    id_horario: int
    bloque: str

    @validator('bloque')
    def validar_bloque(cls, v):
        if not re.match(r"^\d{2}:\d{2}-\d{2}:\d{2}$", v):
            raise ValueError("Formato de bloque horario inválido.")
        return v

class ParametrosModel(BaseModel):
    delta: float
    lambda_penalizacion: float
    aulas: List[AulaModel]
    grupos: List[GrupoModel]
    horarios: List[HorarioModel]
