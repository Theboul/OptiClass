import tkinter as tk
from tkinter import ttk, messagebox
from core.ResultadoAsignacion import ResultadoAsignacion

class ResultsDialog:
    def __init__(self, parent):
        """
        Diálogo para mostrar resultados de asignación de aulas/horarios.
        
        Args:
            parent: Ventana padre (MainWindow)
        """
        self.parent = parent
        self._configure_styles()

    def _configure_styles(self):
        """Configura estilos consistentes con la aplicación"""
        self.style = ttk.Style()
        self.style.configure('Results.TLabel', font=('Segoe UI', 10))
        self.style.configure('Results.TButton', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 9, 'bold'))

    def mostrar_resultados_simple(self, resultado):
        """
        Muestra resultados básicos en un messagebox.
        
        Args:
            resultado (ResultadoAsignacion): Resultados a mostrar
        """
        if not self._validar_resultado(resultado):
            return

        texto = [
            f"Valor objetivo: {resultado.valor_objetivo}\n",
            "\nAsignaciones:\n"
        ]
        
        for asign in resultado.asignaciones:
            texto.append(
                f"• Grupo {asign.grupo.id_grupo} ({asign.grupo.materia}) → "
                f"Aula {asign.aula.id_aula} (Piso {asign.aula.piso}) @ "
                f"{asign.horario.bloque}\n"
            )

        messagebox.showinfo(
            "Resultados de Asignación",
            "".join(texto)
        )

    def mostrar_resultados_detallados(self, resultado):
        """
        Muestra resultados completos en ventana emergente con tabla.
        
        Args:
            resultado (Resultado): Resultados a mostrar
        """
        if not self._validar_resultado(resultado):
            return

        # Configurar ventana emergente
        dialog = tk.Toplevel(self.parent)
        dialog.title("Resultados Detallados")
        dialog.geometry("800x500")
        dialog.resizable(True, True)
        dialog.transient(self.parent)
        dialog.grab_set()

        # Frame principal
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Mostrar valor objetivo
        self._mostrar_valor_objetivo(main_frame, resultado)

        # Crear tabla scrollable
        table_frame = self._crear_tabla_resultados(main_frame, resultado)

        # Botón de cierre
        ttk.Button(
            main_frame,
            text="Cerrar",
            style='Results.TButton',
            command=dialog.destroy
        ).pack(pady=(10, 0))

    def _validar_resultado(self, resultado):
        """Valida que el resultado sea correcto"""
        if not resultado or not isinstance(resultado, ResultadoAsignacion):
            messagebox.showerror(
                "Error", 
                "No hay resultados válidos para mostrar"
            )
            return False
        return True

    def _mostrar_valor_objetivo(self, parent, resultado):
        """Muestra el valor objetivo del resultado"""
        ttk.Label(
            parent,
            text=f"Función Objetivo: {resultado.valor_objetivo}",
            style='Results.TLabel',
            font=('Segoe UI', 10, 'bold')
        ).pack(pady=(0, 10))

    def _crear_tabla_resultados(self, parent, resultado):
        """Crea la tabla scrollable con los resultados y muestra métricas fuera del scroll."""

        # Contenedor principal
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)

        # --- Canvas y Scrollbars ---
        canvas = tk.Canvas(container, highlightthickness=0)
        y_scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        x_scrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

        canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Encabezados ---
        headers = [
            ("Grupo", 5), ("Materia", 15), ("Estudiantes", 10),
            ("Aula", 5), ("Capacidad", 10), ("Piso", 5), ("Horario", 15),
            ("Espacio libre", 10), ("Subutilización", 14), ("% Utilización", 14)
        ]

        for col, (header, width) in enumerate(headers):
            ttk.Label(
                scrollable_frame, text=header, style='Header.TLabel', width=width
            ).grid(row=0, column=col, padx=2, pady=2, sticky=tk.EW)

        # --- Cálculos ---
        delta = resultado.parametros.delta
        lambda_ = resultado.parametros.lambda_penalizacion
        total_porcentaje = 0
        total_subutilizacion = 0
        total_asignaciones = len(resultado.asignaciones)
        total_estudiantes_asignados = 0

        for row, asign in enumerate(resultado.asignaciones, 1):
            grupo = asign.grupo
            aula = asign.aula
            horario = asign.horario

            espacio_libre = aula.capacidad - grupo.cantidad_estudiantes
            subutilizacion = max(0, espacio_libre - (delta * aula.capacidad))
            porcentaje_utilizacion = (grupo.cantidad_estudiantes / aula.capacidad) * 100

            total_porcentaje += porcentaje_utilizacion
            total_subutilizacion += subutilizacion
            total_estudiantes_asignados += grupo.cantidad_estudiantes

            datos = [
                grupo.id_grupo, grupo.materia, grupo.cantidad_estudiantes,
                aula.id_aula, aula.capacidad, aula.piso, horario.bloque,
                espacio_libre, round(subutilizacion, 2), round(porcentaje_utilizacion, 2)
            ]

            for col, valor in enumerate(datos):
                ttk.Label(
                    scrollable_frame, text=str(valor), style='Results.TLabel'
                ).grid(row=row, column=col, padx=2, pady=2, sticky=tk.EW)

        for col in range(len(headers)):
            scrollable_frame.grid_columnconfigure(col, weight=1)

        # --- Indicadores (fuera del scroll) ---
        promedio_utilizacion = total_porcentaje / total_asignaciones if total_asignaciones else 0
        promedio_subutilizacion = total_subutilizacion / total_asignaciones if total_asignaciones else 0
        penalizacion_total = total_subutilizacion * lambda_

        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.X, padx=10, pady=8)

        indicadores = [
            f"Valor objetivo (Z): {round(resultado.valor_objetivo, 2)}",
            f"Utilización promedio de aulas (%): {round(promedio_utilizacion, 2)}",
            f"Promedio subutilización penalizada: {round(promedio_subutilizacion, 2)}",
            f"Penalización total: {round(penalizacion_total, 2)}",
            f"Penalización por subutilización: {lambda_}"
        ]

        for texto in indicadores:
            ttk.Label(info_frame, text=texto, style='Results.TLabel').pack(anchor="w")

        return container