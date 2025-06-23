from interfaz.components.AppMenuBar import AppMenuBar
from interfaz.components.ScrollableTable import ScrollableTable
from interfaz.dialogs.FileDialogs import FileDialogs
from interfaz.dialogs.ResultsDialog import ResultsDialog
from interfaz.forms.InitialSetupForm import InitialSetupForm
from interfaz.forms.PenaltyParametersForm import PenaltyParametersForm
from core.Grupo import Grupo
from core.Aula import Aula
from core.Horario import Horario
from core.Parametros import Parametros
from Solver_MILP.ModeloAsignacion import ModeloAsignacion
from utils.Utilidades import obtener_ruta_recurso

import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.parametros = None
        self.resultado = None
        
        # Configuración inicial
        self.root.title("OptiClass - Asignación de aulas y horarios")
        self.root.configure(bg="#2c2c2c")
        self._configurar_estilos()
        self._configurar_ventana_principal()
        
        # Inicializar componentes
        self.file_dialogs = FileDialogs(self)
        self.results_dialog = ResultsDialog(self.root)
        
        self.menu_bar = AppMenuBar(self.root, self)
        
        # Contenedor principal
        self.contenedor_formulario = ttk.Frame(self.root)
        self.contenedor_formulario.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Formularios
        self.setup_form = InitialSetupForm(self.contenedor_formulario, self)
        self.penalty_form = PenaltyParametersForm(self.contenedor_formulario, self)
        
        # icono y mensaje inicial
        ruta_icono = obtener_ruta_recurso("assets/icon.ico")
        self._icono_ventana(ruta_icono)
        self.label_inicio = ttk.Label(
            self.contenedor_formulario, 
            text="Seleccione 'New / Nuevo' o cargue un archivo .json o Excel(.cvs) para comenzar."
        )
        self.label_inicio.pack(pady=20)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="white",
            background="#007ACC",
            padding=6
        )
        style.map("TButton",
            background=[
                ('active', '#005F9E'),   
                ('pressed', '#004C7A')   
            ],
            foreground=[
                ('disabled', '#cccccc')  
            ]
        )
        
        style.configure("Accent.TButton",
            background="#28A745",
            foreground="white",
            font=('Segoe UI', 10, 'bold'),
            padding=6
        )
        style.map("Accent.TButton",
            background=[
                ('active', '#218838'),
                ('pressed', '#1e7e34')
            ],
            foreground=[
                ('disabled', '#cccccc')
            ]
        )

    def _configurar_ventana_principal(self):
        w, h = 1000, 700
        self.root.geometry(f"{w}x{h}+{(self.root.winfo_screenwidth() - w)//2}+{(self.root.winfo_screenheight() - h)//2}")

    def _icono_ventana(self, ruta_icono):
        """
        Establece el ícono de la ventana principal para Windows (.ico válido).

        Args:
            ruta_icono (str): Ruta absoluta al archivo .ico
        """
        import os
        if not os.path.exists(ruta_icono):
            raise FileNotFoundError(f"Icono no encontrado: {ruta_icono}")
        
        self.root.iconbitmap(ruta_icono)

    def _limpiar_tablas(self):
        for widget in self.contenedor_formulario.winfo_children():
            widget.destroy()
        self.setup_form = InitialSetupForm(self.contenedor_formulario, self)
        self.penalty_form = PenaltyParametersForm(self.contenedor_formulario, self)


    def new_form(self):
        self._limpiar_tablas()
        self.setup_form.mostrar_formulario_inicial()
        self.setup_form.pack(fill="both", expand=True)


    def generar_tablas(self, datos):
        """Genera las tablas con los parámetros iniciales"""
        self._limpiar_tablas()
        
        try:
            # Crear tablas scrollables
            self.grupo_entries = ScrollableTable(
                self.contenedor_formulario, 
                "Grupos", 
                ["Grupo", "Materia", "Nro Alumnos"], 
                datos['grupos']
            )
            self.grupo_entries.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

            self.aula_entries = ScrollableTable(
                self.contenedor_formulario, 
                "Aulas", 
                ["Aula", "Capacidad", "Piso"], 
                datos['aulas']
            )
            self.aula_entries.grid(row=0, column=4, columnspan=4, padx=5, pady=5, sticky="nsew")

            self.horario_entries = ScrollableTable(
                self.contenedor_formulario, 
                "Horarios", 
                ["Horario", "Hora Inicio", "Hora Final"], 
                datos['horarios']
            )
            self.horario_entries.grid(row=0, column=8, columnspan=4, padx=5, pady=5, sticky="nsew")

            # Mostrar formulario de parámetros de penalización
            self.penalty_form.grid(
                row=1, column=0, columnspan=12, 
                padx=10, pady=10, sticky="ew"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar tablas: {str(e)}")


    def resolver(self, delta=None, lambda_penalizacion=None):
        """Resuelve el problema de asignación"""
        try:
            # Obtener parámetros si no se proporcionaron
            if delta is None or lambda_penalizacion is None:
                delta, lambda_penalizacion = self.penalty_form.obtener_valores()
            
            # Obtener datos de las tablas
            grupos = []
            for fila in self.grupo_entries.obtener_datos():
                grupos.append(Grupo(
                    int(fila[0].strip()),
                    int(fila[2].strip()),
                    fila[1].strip()
                ))
            
            aulas = []
            for fila in self.aula_entries.obtener_datos():
                aulas.append(Aula(
                    int(fila[0].strip()),
                    int(fila[1].strip()),
                    int(fila[2].strip())
                ))
            
            horarios = []
            for fila in self.horario_entries.obtener_datos():
                horarios.append(Horario(
                    int(fila[0].strip()),
                    f"{fila[1].strip()}-{fila[2].strip()}"
                ))
            
            # Crear y resolver modelo
            self.parametros = Parametros(
                delta, lambda_penalizacion, aulas, grupos, horarios
            )
            modelo = ModeloAsignacion(self.parametros)
            self.resultado = modelo.resolver()
            
            # Mostrar resultados
            self.results_dialog.mostrar_resultados_detallados(self.resultado)
            
        except Exception as e:
            import traceback
            messagebox.showerror(
                "Error", 
                f"Ocurrió un error:\n{str(e)}\n\n{traceback.format_exc()}"
            )


    def cargar_datos_desde_parametros(self, parametros):
        """Carga datos desde un objeto Parametros"""
        self.parametros = parametros
        self._limpiar_tablas()
        
        # Configurar entradas iniciales
        self.entradas = {
            'grupos': tk.StringVar(value=str(len(parametros.grupos))),
            'aulas': tk.StringVar(value=str(len(parametros.aulas))),
            'horarios': tk.StringVar(value=str(len(parametros.horarios)))
        }
        
        # Generar la UI
        self.generar_tablas({
            'grupos': len(parametros.grupos),
            'aulas': len(parametros.aulas),
            'horarios': len(parametros.horarios)
        })
        
        # Rellenar datos
        for i, grupo in enumerate(parametros.grupos):
            self.grupo_entries.entradas[i][0].insert(0, str(grupo.id_grupo))
            self.grupo_entries.entradas[i][1].insert(0, grupo.materia)
            self.grupo_entries.entradas[i][2].insert(0, str(grupo.cantidad_estudiantes))
        
        for i, aula in enumerate(parametros.aulas):
            self.aula_entries.entradas[i][0].insert(0, str(aula.id_aula))
            self.aula_entries.entradas[i][1].insert(0, str(aula.capacidad))
            self.aula_entries.entradas[i][2].insert(0, str(aula.piso))
        
        for i, horario in enumerate(parametros.horarios):
            self.horario_entries.entradas[i][0].insert(0, str(horario.id_horario))
            inicio, fin = horario.bloque.split("-")
            self.horario_entries.entradas[i][1].insert(0, inicio)
            self.horario_entries.entradas[i][2].insert(0, fin)
        
        # Establecer parámetros de penalización
        self.penalty_form.establecer_valores(
            parametros.delta,
            parametros.lambda_penalizacion
        )


    def cargar_datos_desde_dataframes(self, df_grupos, df_aulas, df_horarios, parametros):
        """Carga datos desde DataFrames"""
        self.parametros = Parametros(
            delta=parametros["delta"],
            lambda_penalizacion=parametros["lambda"],
            aulas=[Aula(row["Aula"], row["Capacidad"], row["Piso"]) for _, row in df_aulas.iterrows()],
            grupos=[Grupo(row["Grupo"], row["Estudiantes"], row["Materia"]) for _, row in df_grupos.iterrows()],
            horarios=[Horario(row["Horario"], row["Bloque"]) for _, row in df_horarios.iterrows()]
        )
        
        self._limpiar_tablas()
        
        # Configurar entradas iniciales
        self.entradas = {
            'grupos': tk.StringVar(value=str(len(df_grupos))),
            'aulas': tk.StringVar(value=str(len(df_aulas))),
            'horarios': tk.StringVar(value=str(len(df_horarios)))
        }
        
        # Generar la UI
        self.generar_tablas({
            'grupos': len(df_grupos),
            'aulas': len(df_aulas),
            'horarios': len(df_horarios)
        })
        
        # Rellenar datos
        for i, row in df_grupos.iterrows():
            self.grupo_entries.entradas[i][0].insert(0, str(row["Grupo"]))
            self.grupo_entries.entradas[i][1].insert(0, row["Materia"])
            self.grupo_entries.entradas[i][2].insert(0, str(row["Estudiantes"]))
        
        for i, row in df_aulas.iterrows():
            self.aula_entries.entradas[i][0].insert(0, str(row["Aula"]))
            self.aula_entries.entradas[i][1].insert(0, str(row["Capacidad"]))
            self.aula_entries.entradas[i][2].insert(0, str(row["Piso"]))
        
        for i, row in df_horarios.iterrows():
            self.horario_entries.entradas[i][0].insert(0, str(row["Horario"]))
            if "-" in row["Bloque"]:
                inicio, fin = row["Bloque"].split("-")
            else:
                inicio, fin = "", ""
            self.horario_entries.entradas[i][1].insert(0, inicio)
            self.horario_entries.entradas[i][2].insert(0, fin)
        
        # Establecer parámetros de penalización
        self.penalty_form.establecer_valores(
            parametros["delta"],
            parametros["lambda"]
        )


def iniciar_interfaz():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()