
from ortools.linear_solver import pywraplp
from core.Aula import Aula
from core.Grupo import Grupo
from core.Horario import Horario
from core.Parametros import Parametros
from core.Asignacion import Asignacion
from core.ResultadoAsignacion import ResultadoAsignacion

class ModeloAsignacion:
    def __init__(self, parametros):
        self.parametros = parametros

    def resolver(self):
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            raise Exception("No se pudo crear el solver SCIP.")

        aulas = self.parametros.aulas
        grupos = self.parametros.grupos
        horarios = self.parametros.horarios
        delta = self.parametros.delta
        lambda_penalizacion = self.parametros.lambda_penalizacion

        x = {}
        U = {}

        # Crear variables
        for g_idx, grupo in enumerate(grupos):
            for a_idx, aula in enumerate(aulas):
                for h_idx, horario in enumerate(horarios):
                    x[g_idx, a_idx, h_idx] = solver.BoolVar(f'x_{g_idx}_{a_idx}_{h_idx}')
                    U[g_idx, a_idx, h_idx] = solver.NumVar(0.0, solver.infinity(), f'U_{g_idx}_{a_idx}_{h_idx}')

        # Restricciones
        # Cada grupo se asigna una vez
        for g_idx in range(len(grupos)):
            solver.Add(solver.Sum([x[g_idx, a_idx, h_idx] for a_idx in range(len(aulas)) for h_idx in range(len(horarios))]) == 1)

        # Cada aula-horario recibe a lo sumo un grupo
        for a_idx in range(len(aulas)):
            for h_idx in range(len(horarios)):
                solver.Add(solver.Sum([x[g_idx, a_idx, h_idx] for g_idx in range(len(grupos))]) <= 1)

        # Restricciones de capacidad
        for g_idx, grupo in enumerate(grupos):
            for a_idx, aula in enumerate(aulas):
                for h_idx, horario in enumerate(horarios):
                    if grupo.cantidad_estudiantes > aula.capacidad:
                        solver.Add(x[g_idx, a_idx, h_idx] == 0)

        # Definición de U
        for g_idx, grupo in enumerate(grupos):
            for a_idx, aula in enumerate(aulas):
                for h_idx, horario in enumerate(horarios):
                    espacio_libre = aula.capacidad - grupo.cantidad_estudiantes - delta * aula.capacidad
                    if espacio_libre > 0:
                        solver.Add(U[g_idx, a_idx, h_idx] >= espacio_libre * x[g_idx, a_idx, h_idx])
                    else:
                        solver.Add(U[g_idx, a_idx, h_idx] == 0)

        # Función objetivo
        objective = solver.Objective()
        for g_idx, grupo in enumerate(grupos):
            for a_idx, aula in enumerate(aulas):
                for h_idx, horario in enumerate(horarios):
                    objective.SetCoefficient(x[g_idx, a_idx, h_idx], grupo.cantidad_estudiantes)
                    objective.SetCoefficient(U[g_idx, a_idx, h_idx], -lambda_penalizacion)
        objective.SetMaximization()

        # Resolver
        status = solver.Solve()

        asignaciones = []
        valor_objetivo = 0
        if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
            valor_objetivo = objective.Value()
            for g_idx, grupo in enumerate(grupos):
                for a_idx, aula in enumerate(aulas):
                    for h_idx, horario in enumerate(horarios):
                        if x[g_idx, a_idx, h_idx].solution_value() > 0.5:
                            asignaciones.append(Asignacion(grupo, aula, horario))
        else:
            print("No se encontró solución óptima o factible.")

        return ResultadoAsignacion(asignaciones, valor_objetivo)
