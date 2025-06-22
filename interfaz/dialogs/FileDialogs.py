import tkinter as tk
from tkinter import filedialog, messagebox
from utils.Utilidades import guardar_json, cargar_json, guardar_resultado_en_csv, cargar_csv
from core.Parametros import Parametros
import traceback

class FileDialogs:
    def __init__(self, controller):
        """
        Maneja todos los diálogos de archivo de la aplicación.
        
        Args:
            controller: Referencia a la instancia de MainWindow (controlador principal)
        """
        self.controller = controller
        self._configurar_tipos_archivo()

    def _configurar_tipos_archivo(self):
        """Configura los tipos de archivo para los diálogos"""
        self.json_types = [('Archivos JSON', '*.json')]
        self.csv_types = [('Archivos CSV', '*.csv')]
        self.all_types = [('Todos los archivos', '*.*')]

    def cargar_json(self):
        """Maneja el diálogo y proceso de carga de archivos JSON"""
        ruta = filedialog.askopenfilename(
            filetypes=self.json_types + self.all_types,
            title="Seleccionar archivo JSON con parámetros"
        )

        if not ruta:
            return

        try:
            parametros = cargar_json(ruta)
            if not isinstance(parametros, Parametros):
                raise ValueError("El archivo no contiene parámetros válidos")
                
            self.controller.cargar_datos_desde_parametros(parametros)
            messagebox.showinfo(
                "Carga exitosa", 
                "Los parámetros se cargaron correctamente desde el archivo JSON."
            )
        except Exception as e:
            self._mostrar_error_detallado(
                "Error al cargar JSON",
                "No se pudo cargar el archivo JSON con los parámetros.",
                e
            )

    def guardar_json(self, parametros):
        """Maneja el diálogo y proceso de guardado de archivos JSON"""
        if not isinstance(parametros, Parametros):
            messagebox.showerror(
                "Error", 
                "Los parámetros no son válidos para guardar."
            )
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=self.json_types,
            title="Guardar parámetros como JSON",
            initialfile="parametros_aulas"
        )

        if ruta:
            try:
                guardar_json(parametros, ruta)
                messagebox.showinfo(
                    "Guardado exitoso",
                    f"Los parámetros se guardaron correctamente en:\n{ruta}"
                )
            except Exception as e:
                self._mostrar_error_detallado(
                    "Error al guardar",
                    "No se pudieron guardar los parámetros en el archivo JSON.",
                    e
                )

    def cargar_csv(self):
        """Maneja el diálogo y proceso de carga de archivos CSV"""
        ruta = filedialog.askopenfilename(
            filetypes=self.csv_types + self.all_types,
            title="Seleccionar archivo CSV con datos"
        )

        if not ruta:
            return

        try:
            data = cargar_csv(ruta)
            if len(data) != 4:
                raise ValueError("El archivo CSV no tiene el formato correcto")
                
            self.controller.cargar_datos_desde_dataframes(*data)
        except Exception as e:
            self._mostrar_error_detallado(
                "Error al cargar CSV",
                "No se pudo cargar el archivo CSV con los datos.",
                e
            )

    def guardar_csv(self, resultado):
        """Maneja el diálogo y proceso de guardado de archivos CSV"""
        if not resultado or not hasattr(resultado, 'asignaciones'):
            messagebox.showerror(
                "Error", 
                "No hay resultados válidos para guardar. Resuelva el problema primero."
            )
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=self.csv_types,
            title="Guardar resultados como CSV",
            initialfile="resultados_asignacion"
        )

        if ruta:
            try:
                guardar_resultado_en_csv(resultado, ruta)
                messagebox.showinfo(
                    "Guardado exitoso",
                    f"Los resultados se guardaron correctamente en:\n{ruta}"
                )
            except Exception as e:
                self._mostrar_error_detallado(
                    "Error al guardar",
                    "No se pudieron guardar los resultados en el archivo CSV.",
                    e
                )

    def _mostrar_error_detallado(self, titulo, mensaje, error):
        """Muestra un mensaje de error detallado con traza completa"""
        error_msg = f"{mensaje}\n\nError: {str(error)}\n\nDetalles:\n{traceback.format_exc()}"
        messagebox.showerror(titulo, error_msg)