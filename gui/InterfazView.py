from core.Grupo import Grupo
from core.Aula import Aula
from core.Horario import Horario
from core.Parametros import Parametros
from Solver_MILP.ModeloAsignacion import ModeloAsignacion
from utils.Utilidades import guardar_resultado_en_csv, cargar_csv, guardar_json,cargar_json

import tkinter as tk
from tkinter import ttk, filedialog, messagebox



class InterfazView:
    def __init__(self, root):
        self.root = root
        self.parametros = None
        self.root.title("OptiClass - Asignación de aulas y horarios")

        self.menu_principal = tk.Menu(self.root)
        self.root.config(menu=self.menu_principal)

        self._crear_menu()

        self.contenedor_formulario = ttk.Frame(self.root)
        self.contenedor_formulario.pack(padx=10, pady=10, fill="both", expand=True)

        self.label_inicio = ttk.Label(self.contenedor_formulario, text="Seleccione 'New / Nuevo' o cargue un archivo JSON para comenzar.")
        self.label_inicio.pack(pady=20)

    def _crear_menu(self):
        archivo_menu = tk.Menu(self.menu_principal, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.new_form)
        archivo_menu.add_command(label="Cargar Archivo JSON", command=self.cargar_json)
        archivo_menu.add_command(label="Guardar Archivo JSON", command=self.guardar_json)
        archivo_menu.add_command(label="Cargar Archivo CSV", command=self.cargar_csv)
        archivo_menu.add_command(label="Guardar Archivo CSV", command=self.guardar_csv)
        self.menu_principal.add_cascade(label="Archivo", menu=archivo_menu)

    def new_form(self):
        for widget in self.contenedor_formulario.winfo_children():
            widget.destroy()

        self.entradas = {}
        labels = ["Grupos", "Aulas", "Pisos", "Horarios"]

        # Crear marco para inputs
        frame = ttk.LabelFrame(self.contenedor_formulario, text="Parámetros iniciales")
        frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        for i, label in enumerate(labels):
            entrada = self._crear_input_label(frame, label + ":", 0, i)
            self.entradas[label.lower()] = entrada

        ttk.Button(self.contenedor_formulario, text="Generar tablas", command=self.generar_tablas)\
            .grid(row=1, column=0, columnspan=4, pady=10)

    def _crear_input_label(self, parent, texto, fila, columna, ancho=5):
        ttk.Label(parent, text=texto).grid(row=fila, column=columna, padx=5, pady=2)
        entrada = ttk.Entry(parent, width=ancho)
        entrada.grid(row=fila+1, column=columna, padx=5)
        return entrada

    #Scroll
    def _crear_tabla_scrollable(self, titulo, headers, num_filas, row_start, col_start):
        # Contenedor externo
        contenedor = ttk.Frame(self.contenedor_formulario)
        contenedor.grid(row=row_start, column=col_start, columnspan=len(headers), padx=5, pady=5, sticky="nsew")

        # Título
        ttk.Label(contenedor, text=titulo).pack()

        # Canvas + Scrollbar
        canvas = tk.Canvas(contenedor, height=300)
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame dentro del canvas
        frame_scroll = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")

        # Usamos lambda para evitar problemas de scope
        frame_scroll.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        # Encabezados
        for i, h in enumerate(headers):
            ttk.Label(frame_scroll, text=h).grid(row=0, column=i, padx=2, pady=2)

        # Entradas
        entradas = []
        for i in range(num_filas):
            fila = []
            for j in range(len(headers)):
                e = ttk.Entry(frame_scroll, width=12)
                e.grid(row=i+1, column=j, padx=1, pady=1)
                fila.append(e)
            entradas.append(fila)

        return entradas


    def _limpiar_tablas(self):
        for widget in self.contenedor_formulario.winfo_children():
            widget.destroy()

    # tabla
    def _crear_tabla(self, titulo, headers, num_filas, row_start, col_start):
        ttk.Label(self.contenedor_formulario, text=titulo).grid(row=row_start, column=col_start, columnspan=len(headers))
        for i, h in enumerate(headers):
            ttk.Label(self.contenedor_formulario, text=h).grid(row=row_start+1, column=col_start+i)
        entradas = []
        for i in range(num_filas):
            fila = []
            for j in range(len(headers)):
                e = ttk.Entry(self.contenedor_formulario, width=12)
                e.grid(row=row_start+2+i, column=col_start+j)
                fila.append(e)
            entradas.append(fila)
        return entradas
    
    def generar_tablas(self):
        try:
            grupos = int(self.entradas['grupos'].get())
            aulas = int(self.entradas['aulas'].get())
            horarios = int(self.entradas['horarios'].get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese números válidos")
            return

        start_row = 4

        self.grupo_entries = self._crear_tabla_scrollable("Grupos", ["Grupo", "Materia", "Nro Alumnos"], grupos, start_row, 0)
        self.aula_entries = self._crear_tabla_scrollable("Aulas", ["Aula", "Capacidad", "Piso"], aulas, start_row, 4)
        self.horario_entries = self._crear_tabla_scrollable("Horarios", ["Horario", "Hora Inicio", "Hora Final"], horarios, start_row, 8)

        # Parámetros adicionales: delta y lambda
        fila_parametros = start_row + 2 + max(grupos, aulas, horarios)
        ttk.Label(self.contenedor_formulario, text="Delta (subutilización)").grid(row=fila_parametros, column=0, columnspan=2)
        self.entry_delta = ttk.Entry(self.contenedor_formulario, width=10)
        self.entry_delta.insert(0, "0.2")
        self.entry_delta.grid(row=fila_parametros+1, column=0, columnspan=2)

        ttk.Label(self.contenedor_formulario, text="Lambda (penalización)").grid(row=fila_parametros, column=2, columnspan=2)
        self.entry_lambda = ttk.Entry(self.contenedor_formulario, width=10)
        self.entry_lambda.insert(0, "10")
        self.entry_lambda.grid(row=fila_parametros+1, column=2, columnspan=2)

        # Ahora botón resolver más abajo
        ttk.Button(self.contenedor_formulario, text="Resolver", command=self.resolver).grid(
            row=fila_parametros+2, column=0, columnspan=12, pady=10)


    def resolver(self):
        try:
            # Grupos
            grupos = []
            for fila in self.grupo_entries:
                id_grupo = int(fila[0].get().strip())
                if id_grupo <= 0:
                    raise ValueError("ID del grupo debe ser un entero positivo.")

                cantidad = int(fila[2].get().strip())
                if cantidad <= 0:
                    raise ValueError("Cantidad de estudiantes debe ser un entero positivo.")

                materia = fila[1].get().strip()
                if not materia:
                    raise ValueError("Materia no puede estar vacía.")

                grupos.append(Grupo(id_grupo, cantidad, materia))

            # Aulas
            aulas = []
            for fila in self.aula_entries:
                id_aula = int(fila[0].get().strip())
                capacidad = int(fila[1].get().strip())
                piso = int(fila[2].get().strip())
                aulas.append(Aula(id_aula, capacidad, piso))

            # Horarios
            horarios = []
            for fila in self.horario_entries:
                id_horario = int(fila[0].get().strip())
                hora_inicio = fila[1].get().strip()
                hora_fin = fila[2].get().strip()
                if not hora_inicio or not hora_fin:
                    raise ValueError("Horas de inicio y fin no pueden estar vacías.")
                bloque = f"{hora_inicio}-{hora_fin}"
                horarios.append(Horario(id_horario, bloque))

            # Parámetros
            try:
                delta = float(self.entry_delta.get())
                lambda_penalizacion = float(self.entry_lambda.get())
            except ValueError:
                raise ValueError("Delta y Lambda deben ser valores numéricos válidos.")
            self.parametros = Parametros(delta, lambda_penalizacion, aulas, grupos, horarios)

            # Modelo y solución
            modelo = ModeloAsignacion(self.parametros)
            self.resultado = modelo.resolver()

            # Mostrar resultados
            texto = f"Valor objetivo: {self.resultado.valor_objetivo}\n\nAsignaciones:\n"
            for asign in self.resultado.asignaciones:
                texto += (f"Grupo {asign.grupo.id_grupo} → Aula {asign.aula.id_aula} "
                        f"en horario {asign.horario.id_horario}\n")

            messagebox.showinfo("Resultado", texto)

        except Exception as e:
            import traceback
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}\n{traceback.format_exc()}")

# Cargar y Guardar en Json
    def cargar_json(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivo JSON", "*.json")],
            title="Cargar archivo JSON"
        )

        if ruta:
            try:
                self.parametros = cargar_json(ruta)

                # Paso 1: Limpiar interfaz y preparar entradas
                self._limpiar_tablas()
                self.entradas = {
                    'grupos': tk.StringVar(),
                    'aulas': tk.StringVar(),
                    'horarios': tk.StringVar()
                }
                self.entradas['grupos'].set(str(len(self.parametros.grupos)))
                self.entradas['aulas'].set(str(len(self.parametros.aulas)))
                self.entradas['horarios'].set(str(len(self.parametros.horarios)))

                # Crear formulario según la cantidad
                self.generar_tablas()

                # Paso 2: Rellenar datos de Grupos
                for i, grupo in enumerate(self.parametros.grupos):
                    self.grupo_entries[i][0].insert(0, grupo.id_grupo)
                    self.grupo_entries[i][1].insert(0, grupo.materia)  # Asegúrate que sea .materia
                    self.grupo_entries[i][2].insert(0, grupo.cantidad_estudiantes)

                # Paso 3: Rellenar datos de Aulas
                for i, aula in enumerate(self.parametros.aulas):
                    self.aula_entries[i][0].insert(0, aula.id_aula)
                    self.aula_entries[i][1].insert(0, aula.capacidad)
                    self.aula_entries[i][2].insert(0, aula.piso)

                # Paso 4: Rellenar datos de Horarios
                for i, horario in enumerate(self.parametros.horarios):
                    self.horario_entries[i][0].insert(0, horario.id_horario)
                    inicio, fin = horario.bloque.split("-")
                    self.horario_entries[i][1].insert(0, inicio)
                    self.horario_entries[i][2].insert(0, fin)

                # Paso 5: Rellenar delta y lambda
                self.entry_delta.delete(0, tk.END)
                self.entry_delta.insert(0, str(self.parametros.delta))

                self.entry_lambda.delete(0, tk.END)
                self.entry_lambda.insert(0, str(self.parametros.lambda_penalizacion))

                messagebox.showinfo("Éxito", "Datos cargados correctamente.")

            except Exception as e:
                import traceback
                messagebox.showerror("Error", f"Ocurrió un error al cargar:\n{str(e)}\n\n{traceback.format_exc()}")


    def guardar_json(self):
     if not self.parametros:
        messagebox.showerror("Error", "No hay datos para guardar.")
        return

     ruta = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivo JSON", "*.json")],
        title="Guardar como JSON"
     )

     if ruta:
        try:
            guardar_json(self.parametros, ruta)
            messagebox.showinfo("Éxito", "Datos guardados correctamente en JSON.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")

# Cargar y Guardar en CVS
    def cargar_csv(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("CSV files", "*.csv")])
        if not ruta:
            return

        df_grupos, df_aulas, df_horarios, parametros = cargar_csv(ruta)

        # Paso 1: Limpiar interfaz
        self._limpiar_tablas()

        # Paso 2: Preparar self.entradas igual que en JSON
        self.entradas = {
            'grupos': tk.StringVar(value=str(len(df_grupos))),
            'aulas': tk.StringVar(value=str(len(df_aulas))),
            'horarios': tk.StringVar(value=str(len(df_horarios)))
        }

        # Paso 3: Generar la UI con los nuevos valores
        self.generar_tablas()

        # Paso 4: Rellenar tabla de grupos
        for i, row in df_grupos.iterrows():
            self.grupo_entries[i][0].insert(0, row["Grupo"])
            self.grupo_entries[i][1].insert(0, row["Materia"])
            self.grupo_entries[i][2].insert(0, row["Estudiantes"])

        # Paso 5: Rellenar tabla de aulas
        for i, row in df_aulas.iterrows():
            self.aula_entries[i][0].insert(0, row["Aula"])
            self.aula_entries[i][1].insert(0, row["Capacidad"])
            self.aula_entries[i][2].insert(0, row["Piso"])

        # Paso 6: Rellenar tabla de horarios
        for i, row in df_horarios.iterrows():
            self.horario_entries[i][0].insert(0, row["Horario"])
            if "-" in row["Bloque"]:
                inicio, fin = row["Bloque"].split("-")
            else:
                inicio, fin = "", ""
            self.horario_entries[i][1].insert(0, inicio)
            self.horario_entries[i][2].insert(0, fin)

        # Paso 7: Rellenar delta y lambda
        self.entry_delta.delete(0, "end")
        self.entry_delta.insert(0, str(parametros["delta"]))

        self.entry_lambda.delete(0, "end")
        self.entry_lambda.insert(0, str(parametros["lambda"]))
    
    
    def guardar_csv(self):
     if not hasattr(self, 'resultado') or self.resultado is None:
        messagebox.showerror("Error", "Primero debes resolver el problema antes de guardar el resultado.")
        return

     ruta = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Archivos CSV", "*.csv")],
        title="Guardar como"
     )

     if ruta:
         try:
            guardar_resultado_en_csv(self.resultado, ruta)
            messagebox.showinfo("Éxito", f"Resultado guardado correctamente en:\n{ruta}")
         except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

def iniciar_interfaz():
    root = tk.Tk()
    app = InterfazView(root)
    root.mainloop()