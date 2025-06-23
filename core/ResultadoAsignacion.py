from core.Asignacion import Asignacion
from core.Parametros import Parametros
from typing import List

# === Clase ResultadoAsignacion ===
class ResultadoAsignacion:
    #Constructor de la Clase ResultadosAsignacion: Representa los resultados obtenidos tras ejecutar el modelo de asignación.
    def __init__(self, asignaciones: List['Asignacion'], valor_objetivo: float, parametros: 'Parametros'):
       if asignaciones is None:
            raise ValueError("La lista de asignaciones no puede ser nula.")
       if not all(isinstance(a, Asignacion) for a in asignaciones):
            raise TypeError("Todas las asignaciones deben ser instancias de Asignacion.")
       
       self._asignaciones = asignaciones.copy()
       self._valor_objetivo = valor_objetivo
       self._parametros = parametros

    @property
    def asignaciones(self) -> List['Asignacion']:
        return self._asignaciones.copy()

    @property
    def valor_objetivo(self) -> float:
        return self._valor_objetivo   
    
    @property
    def parametros(self) -> 'Parametros':
        return self._parametros

    def mostrar_resultado(self):
        print("==== Resultado de la Asignación ====")
        print(f"Valor objetivo (Z): {self.valor_objetivo}")
        print("\n--- Asignaciones ---")
        for asignacion in self.asignaciones:
            espacio_libre = asignacion.aula.capacidad - asignacion.grupo.cantidad_estudiantes
            subutilizacion = max(0, espacio_libre - (self.parametros.delta * asignacion.aula.capacidad))
            print(
                f"Grupo {asignacion.grupo.id_grupo} ({asignacion.grupo.materia}) → "
                f"Aula {asignacion.aula.id_aula} (Piso {asignacion.aula.piso}, Cap: {asignacion.aula.capacidad}) → "
                f"Horario {asignacion.horario.bloque} | "
                f"Espacio libre: {espacio_libre} | "
                f"Subutilización penalizada: {subutilizacion:.2f}"
            )
        
        # Métricas globales
        utilizacion_promedio = sum(
            (a.grupo.cantidad_estudiantes / a.aula.capacidad) * 100 
            for a in self.asignaciones
        ) / len(self.asignaciones)
        
        print("\n--- Métricas Globales ---")
        print(f"Utilización promedio de aulas: {utilizacion_promedio:.2f}%")
        print(f"Total estudiantes asignados: {self.valor_objetivo}")
    
    def __str__(self):
        return f"ResultadoAsignacion(valor_objetivo={self.valor_objetivo}, asignaciones={self.asignaciones})"