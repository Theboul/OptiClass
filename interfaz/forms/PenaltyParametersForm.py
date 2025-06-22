import tkinter as tk
from tkinter import ttk, messagebox

class PenaltyParametersForm:
    def __init__(self, parent, controller):
        """
        Formulario para parámetros de penalización (delta y lambda).
        
        Args:
            parent: Widget padre (Frame contenedor de MainWindow)
            controller: Referencia a MainWindow (controlador principal)
        """
        self.parent = parent
        self.controller = controller
        
        # Frame principal
        self.frame = ttk.Frame(self.parent)
        self._configurar_estilos()
        self._crear_widgets()

    def _configurar_estilos(self):
        """Configura estilos consistentes con la aplicación"""
        self.style = ttk.Style()
        self.style.configure('Penalty.TLabel', font=('Segoe UI', 9))
        self.style.configure('Penalty.TEntry', font=('Segoe UI', 9))
        self.style.configure('Penalty.TButton', font=('Segoe UI', 10, 'bold'))

    def _crear_widgets(self):
        """Crea y configura los widgets del formulario"""
        # Frame para parámetros
        param_frame = ttk.LabelFrame(
            self.frame,
            text="Parámetros de Penalización",
            padding=(10, 5)
        )
        param_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Configurar Delta
        self._crear_campo_parametro(
            param_frame, 
            "Delta (subutilización):", 
            "0.2", 
            0, 0
        )
        
        # Configurar Lambda
        self._crear_campo_parametro(
            param_frame, 
            "Lambda (penalización):", 
            "10", 
            0, 2
        )
        
        # Botón Resolver
        ttk.Button(
            self.frame,
            text="Resolver Asignación",
            style='Accent.TButton',
            command=self._validar_y_resolver
        ).grid(row=1, column=0, pady=10, sticky="ew")

    def _crear_campo_parametro(self, parent, label_text, default_value, row, column):
        """Crea un campo de parámetro con su etiqueta"""
        ttk.Label(
            parent,
            text=label_text,
            style='Penalty.TLabel'
        ).grid(row=row, column=column, padx=5, pady=2, sticky="w")
        
        entry = ttk.Entry(
            parent,
            width=8,
            style='Penalty.TEntry'
        )
        entry.insert(0, default_value)
        entry.grid(row=row, column=column+1, padx=5, pady=2, sticky="ew")
        
        # Guardar referencia a los entries
        if "Delta" in label_text:
            self.entry_delta = entry
        else:
            self.entry_lambda = entry

    def _validar_y_resolver(self):
        """Valida los parámetros y llama al controlador para resolver"""
        try:
            delta = self._validar_parametro(
                self.entry_delta.get(),
                "Delta",
                min_val=0,
                max_val=1
            )
            
            lambda_penal = self._validar_parametro(
                self.entry_lambda.get(),
                "Lambda",
                min_val=0
            )
            
            self.controller.resolver(delta, lambda_penal)
            
        except ValueError as e:
            messagebox.showerror(
                "Error en Parámetros",
                str(e),
                parent=self.parent
            )

    def _validar_parametro(self, valor, nombre, min_val=None, max_val=None):
        """Valida que el parámetro sea un número válido"""
        try:
            num = float(valor.strip())
            
            if min_val is not None and num < min_val:
                raise ValueError(f"{nombre} debe ser mayor o igual a {min_val}")
                
            if max_val is not None and num > max_val:
                raise ValueError(f"{nombre} debe ser menor o igual a {max_val}")
                
            return num
            
        except ValueError:
            raise ValueError(f"{nombre} debe ser un valor numérico válido")

    def obtener_valores(self):
        """
        Obtiene los valores actuales del formulario validados.
        
        Returns:
            tuple: (delta, lambda_penalizacion)
            
        Raises:
            ValueError: Si los valores no son válidos
        """
        delta = self._validar_parametro(
            self.entry_delta.get(),
            "Delta",
            min_val=0,
            max_val=1
        )
        
        lambda_penal = self._validar_parametro(
            self.entry_lambda.get(),
            "Lambda",
            min_val=0
        )
        
        return (delta, lambda_penal)

    def establecer_valores(self, delta, lambda_penalizacion):
        """
        Establece los valores del formulario.
        
        Args:
            delta (float): Valor de delta (0-1)
            lambda_penalizacion (float): Valor de lambda (>=0)
        """
        self.entry_delta.delete(0, tk.END)
        self.entry_delta.insert(0, str(delta))
        
        self.entry_lambda.delete(0, tk.END)
        self.entry_lambda.insert(0, str(lambda_penalizacion))

    def grid(self, **kwargs):
        """Muestra el formulario usando grid"""
        self.frame.grid(**kwargs)

    def pack(self, **kwargs):
        """Muestra el formulario usando pack"""
        self.frame.pack(**kwargs)

    def place(self, **kwargs):
        """Muestra el formulario usando place"""
        self.frame.place(**kwargs)