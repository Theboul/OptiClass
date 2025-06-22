
from core.Parametros import Parametros
from core.ResultadoAsignacion import ResultadoAsignacion

import pandas as pd

import sys
import os
import csv
import json

def cargar_json(path: str) -> Parametros:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Parametros.from_dict(data)


def guardar_json(parametros: Parametros, ruta: str):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(parametros.to_dict(), f, indent=4)


def cargar_csv(ruta_csv):
    with open(ruta_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        grupos, aulas, horarios = [], [], []
        delta, lambda_penalizacion = 0.0, 0.0

        next(reader, None)  # saltar encabezado

        for row in reader:
            if not row or all(c.strip() == "" for c in row):
                continue

            clave = row[0].strip().lower()
            if clave == "delta" and len(row) > 1:
                try:
                    delta = float(row[1])
                except ValueError:
                    pass
                continue

            if clave == "lambda_penalizacion" and len(row) > 1:
                try:
                    lambda_penalizacion = float(row[1])
                except ValueError:
                    pass
                continue

            try:
                grupo_id = int(row[0])
                materia = row[1]
                estudiantes = int(row[2])
                aula_id = int(row[3])
                capacidad = int(row[4])
                piso = int(row[5])
                horario_id = int(row[6])
                bloque = row[7]

                grupos.append([grupo_id, materia, estudiantes])
                aulas.append([aula_id, capacidad, piso])
                horarios.append([horario_id, bloque])
            except (ValueError, IndexError):
                continue

        df_grupos = pd.DataFrame(grupos, columns=["Grupo", "Materia", "Estudiantes"])
        df_aulas = pd.DataFrame(aulas, columns=["Aula", "Capacidad", "Piso"])
        df_horarios = pd.DataFrame(horarios, columns=["Horario", "Bloque"])

        return df_grupos, df_aulas, df_horarios, {
            "delta": delta,
            "lambda": lambda_penalizacion
        }


def guardar_resultado_en_csv(resultado: ResultadoAsignacion, ruta: str):
    with open(ruta, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        # Encabezados
        writer.writerow([
            "Nro Grupo", "Materia", "Estudiantes",
            "Nro Aula", "Capacidad Aula", "Piso Aula",
            "Nro Horario", "Bloque",
            "Espacio libre", "Subutilizacion penalizada",
            "Porcentaje de utilizacion (%)"
        ])

        delta = resultado.parametros.delta
        lambda_ = resultado.parametros.lambda_penalizacion

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
        penalizacion_total = total_subutilizacion * lambda_
        writer.writerow([])
        writer.writerow(["delta", delta])
        writer.writerow(["lambda_penalizacion", lambda_])
        writer.writerow(["Valor funcion objetivo (Z):", round(resultado.valor_objetivo, 2)])
        writer.writerow(["Penalización total aplicada:", round(penalizacion_total, 2)])
        writer.writerow(["Utilizacion promedio de aulas (%):", round(promedio_utilizacion, 2)])
        writer.writerow(["Promedio subutilizacion penalizada:", round(promedio_subutilizacion, 2)]) 


def obtener_ruta_recurso(nombre_archivo):
    """
    Devuelve la ruta absoluta a un recurso, sea en ejecución normal
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, nombre_archivo)