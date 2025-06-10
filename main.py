from core.Aula import Aula
from core.Grupo import Grupo
from core.Horario import Horario
from core.Parametros import Parametros
from Modelo.ModeloAsignacion import ModeloAsignacion

def main():
    # Crear las 16 aulas como dice el enunciado
    aulas = []
    id_aula = 1

    # Piso 1 y 2: 4 aulas de 45, 2 de 60, 2 de 30 (total 8)
    for piso in [1, 2]:
        aulas.extend([
            Aula(id_aula, 45, piso), Aula(id_aula+1, 45, piso),
            Aula(id_aula+2, 45, piso), Aula(id_aula+3, 45, piso),
            Aula(id_aula+4, 60, piso), Aula(id_aula+5, 60, piso),
            Aula(id_aula+6, 30, piso), Aula(id_aula+7, 30, piso)
        ])
        id_aula += 8

    # Piso 3 y 4: 4 aulas de 60, 2 de 40 (total 6)
    for piso in [3, 4]:
        aulas.extend([
            Aula(id_aula, 60, piso), Aula(id_aula+1, 60, piso),
            Aula(id_aula+2, 60, piso), Aula(id_aula+3, 60, piso),
            Aula(id_aula+4, 40, piso), Aula(id_aula+5, 40, piso)
        ])
        id_aula += 6

    # Piso 5: 2 aulas de 120
    aulas.extend([Aula(id_aula, 120, 5), Aula(id_aula+1, 120, 5)])

    # Crear horarios
    bloques = [
        "07:00–09:15", "09:15–11:30", "11:30–13:45",
        "14:00–16:15", "16:15–18:30", "18:30–20:45"
    ]
    horarios = [Horario(i+1, bloque) for i, bloque in enumerate(bloques)]

    # Crear grupos
    grupos = [
        Grupo(1, 35, "Cálculo I"),
        Grupo(2, 50, "Física I"),
        Grupo(3, 120, "Introducción a la Ingeniería"),
        Grupo(4, 40, "Redes I"),
        Grupo(5, 60, "Álgebra Lineal")
    ]

    # Crear parámetros (lambda_penalizacion en lugar de lambda_)
    parametros = Parametros(delta=0.2, lambda_penalizacion=1.0, 
                          aulas=aulas, grupos=grupos, horarios=horarios)

    # Crear instancia del modelo y resolver
    modelo = ModeloAsignacion(parametros)
    resultado = modelo.resolver()

    # Mostrar resultado
    resultado.mostrar_resultado()

if __name__ == "__main__":
    main()