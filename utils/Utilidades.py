import json
from core.Parametros import Parametros

import csv
from core.ResultadoAsignacion import ResultadoAsignacion

def cargar_json(path: str) -> Parametros:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Parametros.from_dict(data)


def guardar_json(parametros: Parametros, ruta: str):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(parametros.to_dict(), f, indent=4)


def guardar_resultado_en_csv(resultado: ResultadoAsignacion, ruta: str):
    with open(ruta, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Encabezados
        writer.writerow([
            "Nro Grupo", "Materia", "Estudiantes",
            "Nro Aula", "Capacidad Aula", "Piso Aula",
            "Nro Horario", "Bloque",
            "Espacio libre", "Subutilización penalizada",
            "Porcentaje de utilización (%)"
        ])

        delta = resultado.parametros.delta

        total_porcentaje = 0
        total_subutilizacion = 0
        total_asignaciones = len(resultado.asignaciones)

        for asignacion in resultado.asignaciones:
            grupo = asignacion.grupo
            aula = asignacion.aula
            horario = asignacion.horario

            espacio_libre = aula.capacidad - grupo.cantidad_estudiantes
            subutilizacion = max(0, espacio_libre - (delta * aula.capacidad))
            porcentaje_utilizacion = (grupo.cantidad_estudiantes / aula.capacidad) * 100

            total_porcentaje += porcentaje_utilizacion
            total_subutilizacion += subutilizacion

            writer.writerow([
                grupo.id_grupo,
                grupo.materia,
                grupo.cantidad_estudiantes,
                aula.id_aula,
                aula.capacidad,
                aula.piso,
                horario.id_horario,
                horario.bloque,
                espacio_libre,
                round(subutilizacion, 2),
                round(porcentaje_utilizacion, 2)
            ])

        # Métricas finales
        promedio_utilizacion = total_porcentaje / total_asignaciones if total_asignaciones > 0 else 0
        promedio_subutilizacion = total_subutilizacion / total_asignaciones if total_asignaciones > 0 else 0

        writer.writerow([])
        writer.writerow(["Valor objetivo (Z):", round(resultado.valor_objetivo, 2)])
        writer.writerow(["Utilización promedio de aulas (%):", round(promedio_utilizacion, 2)])
        writer.writerow(["Promedio subutilización penalizada:", round(promedio_subutilizacion, 2)])

    