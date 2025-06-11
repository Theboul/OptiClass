from core.Aula import Aula
from core.Grupo import Grupo
from core.Horario import Horario
from core.Parametros import Parametros
from Solver_MILP.ModeloAsignacion import ModeloAsignacion

def crear_aulas() -> list[Aula]:
    """Crea las 16 aulas según el enunciado."""
    aulas = []
    id_aula = 1

    # Piso 1 y 2: 4 aulas de 45, 2 de 60, 2 de 30 (total 8 por piso)
    for piso in [1, 2]:
        aulas.extend([
            Aula(id_aula + i, capacidad, piso)
            for i, capacidad in enumerate([45]*4 + [60]*2 + [30]*2)
        ])
        id_aula += 8

    # Piso 3 y 4: 4 aulas de 60, 2 de 40 (total 6 por piso)
    for piso in [3, 4]:
        aulas.extend([
            Aula(id_aula + i, capacidad, piso)
            for i, capacidad in enumerate([60]*4 + [40]*2)
        ])
        id_aula += 6

    # Piso 5: 2 aulas de 120
    aulas.extend([Aula(id_aula, 120, 5), Aula(id_aula + 1, 120, 5)])
    return aulas

def crear_horarios() -> list[Horario]:
    """Crea los 6 bloques horarios sin día."""
    rangos = [
        "07:00-09:15",
        "09:15-11:30",
        "11:30-13:45",
        "14:00-16:15",
        "16:15-18:30",
        "18:30-20:45"
    ]
    return [Horario(i + 1, rango) for i, rango in enumerate(rangos)]

def crear_grupos() -> list[Grupo]:
    """Crea los 5 grupos de estudiantes."""
    return [
        Grupo(1, 35, "Cálculo I"),
        Grupo(2, 50, "Física I"),
        Grupo(3, 120, "Introducción a la Ingeniería"),
        Grupo(4, 40, "Redes I"),
        Grupo(5, 60, "Álgebra Lineal")
    ]

def main():
    try:
        print("=== Inicializando datos ===")
        aulas = crear_aulas()
        horarios = crear_horarios()
        grupos = crear_grupos()

        print(f"- Aulas creadas: {len(aulas)}")
        print(f"- Horarios creados: {len(horarios)}")
        print(f"- Grupos creados: {len(grupos)}")

        print("\n=== Configurando parámetros ===")
        parametros = Parametros(
            delta=0.2,
            lambda_penalizacion=1.0,
            aulas=aulas,
            grupos=grupos,
            horarios=horarios
        )
        print(parametros)

        print("\n=== Resolviendo el modelo ===")
        modelo = ModeloAsignacion(parametros)
        resultado = modelo.resolver()

        print("\n=== Resultados ===")
        resultado.mostrar_resultado()
        # resultado.generar_csv("asignaciones.csv")  # Descomentar si implementado

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()