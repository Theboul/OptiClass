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

        # Variables de decisión
        x = {}  # x[i,j,t] = 1 si grupo i está en aula j en horario t
        U = {}  # U[i,j,t] = espacio subutilizado penalizable

        # Crear variables
        for i in range(len(grupos)):
            for j in range(len(aulas)):
                for t in range(len(horarios)):
                    x[i,j,t] = solver.BoolVar(f'x_{i}_{j}_{t}')
                    U[i,j,t] = solver.NumVar(0.0, solver.infinity(), f'U_{i}_{j}_{t}')

        # Restricciones
        # 1. Cada grupo se asigna exactamente una vez
        for i in range(len(grupos)):
            solver.Add(sum(x[i,j,t] for j in range(len(aulas)) 
                                     for t in range(len(horarios))) == 1)

        # 2. Cada aula-horario tiene como máximo un grupo
        for j in range(len(aulas)):
            for t in range(len(horarios)):
                solver.Add(sum(x[i,j,t] for i in range(len(grupos))) <= 1)

        # 3. Restricción de capacidad del aula
        for i in range(len(grupos)):
            for j in range(len(aulas)):
                for t in range(len(horarios)):
                    solver.Add(x[i,j,t] * grupos[i].cantidad_estudiantes <= aulas[j].capacidad)

        # 4. Definición de espacio subutilizado penalizable
        for i in range(len(grupos)):
            for j in range(len(aulas)):
                for t in range(len(horarios)):
                    espacio_libre = aulas[j].capacidad - grupos[i].cantidad_estudiantes
                    umbral = delta * aulas[j].capacidad
                    # U[i,j,t] >= (espacio_libre - umbral) * x[i,j,t]
                    solver.Add(U[i,j,t] >= (espacio_libre - umbral) * x[i,j,t])
                    # U[i,j,t] >= 0
                    solver.Add(U[i,j,t] >= 0)

        # Función objetivo
        objetivo = solver.Objective()
        # Parte 1: Maximizar estudiantes asignados
        for i in range(len(grupos)):
            for j in range(len(aulas)):
                for t in range(len(horarios)):
                    objetivo.SetCoefficient(x[i,j,t], grupos[i].cantidad_estudiantes)
        # Parte 2: Minimizar espacio subutilizado penalizable
        for i in range(len(grupos)):
            for j in range(len(aulas)):
                for t in range(len(horarios)):
                    objetivo.SetCoefficient(U[i,j,t], -lambda_penalizacion)
        
        objetivo.SetMaximization()

        # Resolver el modelo
        status = solver.Solve()

        # Procesar resultados
        asignaciones = []
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            valor_objetivo = objetivo.Value()
            for i in range(len(grupos)):
                for j in range(len(aulas)):
                    for t in range(len(horarios)):
                        if x[i,j,t].solution_value() > 0.5:
                            asignaciones.append(
                                Asignacion(grupos[i], aulas[j], horarios[t])
                            )
        else:
            print("No se encontró solución óptima o factible.")
            valor_objetivo = 0

        return ResultadoAsignacion(asignaciones, valor_objetivo)