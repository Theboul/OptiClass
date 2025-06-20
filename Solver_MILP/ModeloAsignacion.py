from ortools.linear_solver import pywraplp
from core.Aula import Aula
from core.Grupo import Grupo
from core.Horario import Horario
from core.Parametros import Parametros
from core.Asignacion import Asignacion
from core.ResultadoAsignacion import ResultadoAsignacion
from typing import Dict, Tuple, List

class ModeloAsignacion:
    """Modelo de optimización para asignar grupos a aulas y horarios."""
    
    def __init__(self, parametros: Parametros) -> None:
        self.parametros = parametros
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        if not self.solver:
            raise RuntimeError("No se pudo crear el solver SCIP.")
        self.variables_asignacion: Dict[Tuple[Grupo, Aula, Horario], pywraplp.Variable] = {}
        self.variables_subutilizacion: Dict[Tuple[Grupo, Aula, Horario], pywraplp.Variable] = {}

    def resolver(self) -> ResultadoAsignacion:
        """Ejecuta el modelo y devuelve los resultados."""
        self._crear_variables()
        self._agregar_restricciones()
        self._configurar_objetivo()
        
        status = self.solver.Solve()
        return self._procesar_resultado(status)

    def _crear_variables(self) -> None:
        """Crea las variables de decisión."""
        for grupo in self.parametros.grupos:
            for aula in self.parametros.aulas:
                if grupo.cantidad_estudiantes > aula.capacidad:
                    continue  # Saltar combinaciones inválidas
                for horario in self.parametros.horarios:
                    clave = (grupo, aula, horario)
                    self.variables_asignacion[clave] = self.solver.BoolVar(f'x_{grupo.id_grupo}_{aula.id_aula}_{horario.id_horario}')
                    self.variables_subutilizacion[clave] = self.solver.NumVar(0, self.solver.infinity(), f'U_{grupo.id_grupo}_{aula.id_aula}_{horario.id_horario}')

    def _agregar_restricciones(self) -> None:
        """Agrega todas las restricciones al modelo."""
        self._restriccion_asignacion_unica()
        self._restriccion_aula_horario_unico()
        self._restriccion_capacidad()
        self._restriccion_subutilizacion()

    def _restriccion_asignacion_unica(self) -> None:
        """Cada grupo debe asignarse exactamente una vez."""
        for grupo in self.parametros.grupos:
            variables_grupo = [
                var for (g, a, h), var in self.variables_asignacion.items() 
                if g == grupo
            ]
            self.solver.Add(sum(variables_grupo) == 1)

    def _restriccion_aula_horario_unico(self) -> None:
        """Cada aula-horario puede tener como máximo un grupo."""
        for aula in self.parametros.aulas:
            for horario in self.parametros.horarios:
                variables_aula_horario = [
                    var for (g, a, h), var in self.variables_asignacion.items()
                    if a == aula and h == horario
                ]
                self.solver.Add(sum(variables_aula_horario) <= 1)

    def _restriccion_capacidad(self) -> None:
        """Asegura que los grupos no excedan la capacidad del aula."""
        for (grupo, aula, _), var in self.variables_asignacion.items():
            self.solver.Add(var * grupo.cantidad_estudiantes <= aula.capacidad)

    def _restriccion_subutilizacion(self) -> None:
        """Calcula el espacio subutilizado penalizable."""
        delta = self.parametros.delta
        for (grupo, aula, _), var_x in self.variables_asignacion.items():
            var_u = self.variables_subutilizacion[(grupo, aula, _)]
            espacio_libre = aula.capacidad - grupo.cantidad_estudiantes
            umbral = delta * aula.capacidad
            self.solver.Add(var_u >= (espacio_libre - umbral) * var_x)
            self.solver.Add(var_u >= 0)

    def _configurar_objetivo(self) -> None:
        """Configura la función objetivo."""
        objetivo = self.solver.Objective()
        lambda_penalizacion = self.parametros.lambda_penalizacion
        
        # Maximizar estudiantes asignados
        for (grupo, _, _), var in self.variables_asignacion.items():
            objetivo.SetCoefficient(var, grupo.cantidad_estudiantes)
        
        # Minimizar espacio subutilizado
        for var in self.variables_subutilizacion.values():
            objetivo.SetCoefficient(var, -lambda_penalizacion)
            
        objetivo.SetMaximization()

    def _procesar_resultado(self, status: int) -> ResultadoAsignacion:
        """Convierte la solución del solver en un objeto ResultadoAsignacion."""
        asignaciones = []
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            valor_objetivo = self.solver.Objective().Value()
            for (grupo, aula, horario), var in self.variables_asignacion.items():
                if var.solution_value() > 0.5:
                    asignaciones.append(Asignacion(grupo, aula, horario))
            return ResultadoAsignacion(asignaciones, valor_objetivo, self.parametros)
        raise RuntimeError("No se encontró solución óptima o factible.")