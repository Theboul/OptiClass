from core.Aula import Aula
from core.Grupo import Grupo
from core.Horario import Horario
from typing import List

import pandas as pd

# === Clase Parametros ===
class Parametros:
    #Constructor de la Clase Parametros: Almacena la configuración del problema de optimización
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
    
    @classmethod
    def to_dict(self):
        return {
            "delta": self.delta,
            "lambda_penalizacion": self.lambda_penalizacion,
            "aulas": [a.to_dict() for a in self.aulas],
            "grupos": [g.to_dict() for g in self.grupos],
            "horarios": [h.to_dict() for h in self.horarios]
        }

    @classmethod
    def to_excel(self, ruta: str):
        """Guarda los parámetros en un archivo Excel con varias hojas, validando datos antes de exportar."""
        
        # Validación unificada
        if not self.grupos or not self.aulas or not self.horarios:
            raise ValueError("No se pueden guardar parámetros si faltan grupos, aulas o horarios.")
        
        df_grupos = pd.DataFrame([{
            "Grupo": g.id_grupo,
            "Materia": g.materia,
            "Estudiantes": g.cantidad_estudiantes
        } for g in self.grupos])

        df_aulas = pd.DataFrame([{
            "Aula": a.id_aula,
            "Capacidad": a.capacidad,
            "Piso": a.piso
        } for a in self.aulas])

        df_horarios = pd.DataFrame([{
            "Horario": h.id_horario,
            "Bloque": h.bloque
        } for h in self.horarios])

        df_config = pd.DataFrame({
            "Parametro": ["delta", "lambda_penalizacion"],
            "Valor": [self.delta, self.lambda_penalizacion]
        })

        with pd.ExcelWriter(ruta, engine='openpyxl') as writer:
            df_grupos.to_excel(writer, sheet_name='Grupos', index=False)
            df_aulas.to_excel(writer, sheet_name='Aulas', index=False)
            df_horarios.to_excel(writer, sheet_name='Horarios', index=False)
            df_config.to_excel(writer, sheet_name='Configuracion', index=False)

    @classmethod
    def from_excel(cls, ruta: str) -> 'Parametros':
        xls = pd.read_excel(ruta, sheet_name=None)

        df_grupos = xls.get("Grupos")
        df_aulas = xls.get("Aulas")
        df_horarios = xls.get("Horarios")
        df_config = xls.get("Configuracion")

        # --- Cargar configuración general
        delta = float(df_config[df_config["Parametro"] == "delta"]["Valor"].values[0])
        lambda_penalizacion = float(df_config[df_config["Parametro"] == "lambda_penalizacion"]["Valor"].values[0])

        # --- Cargar grupos con validación robusta
        grupos = []
        for _, r in df_grupos.iterrows():
            id_grupo = int(float(r["Grupo"]))
            estudiantes = int(float(r["Estudiantes"]))
            materia = str(r["Materia"]).strip()
            grupos.append(Grupo(id_grupo, estudiantes, materia))

        # --- Cargar aulas
        aulas = []
        for _, r in df_aulas.iterrows():
            id_aula = int(float(r["Aula"]))
            capacidad = int(float(r["Capacidad"]))
            piso = int(float(r["Piso"]))
            aulas.append(Aula(id_aula, capacidad, piso))

        # --- Cargar horarios
        horarios = []
        for _, r in df_horarios.iterrows():
            id_horario = int(float(r["Horario"]))
            bloque = str(r["Bloque"]).strip()
            horarios.append(Horario(id_horario, bloque))

        # --- Crear instancia de Parametros
        return cls(delta, lambda_penalizacion, aulas, grupos, horarios)
