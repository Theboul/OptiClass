import tkinter as tk
from tkinter import ttk, messagebox

class InitialSetupForm:
    def __init__(self, parent, controller):
        """
        Formulario para la configuración inicial de parámetros.
        
        Args:
            parent: Widget padre (Frame contenedor de MainWindow)
            controller: Referencia a MainWindow (controlador principal)
        """
        self.parent = parent
        self.controller = controller
        self.entradas = {}
        
        # Frame principal
        self.frame = ttk.Frame(self.parent)
        self._configurar_estilos()
        self._crear_interfaz_basica()

    def _configurar_estilos(self):
        """Configura estilos consistentes con la aplicación"""
        self.style = ttk.Style()
        self.style.configure('Form.TLabel', font=('Segoe UI', 9))
        self.style.configure('Form.TEntry', font=('Segoe UI', 9))
        self.style.configure('Form.TButton', font=('Segoe UI', 9, 'bold'))

    def _crear_interfaz_basica(self):
        """Crea los elementos iniciales de la interfaz"""
        self.label_inicio = ttk.Label(
            self.frame,
            text="Seleccione 'Nuevo' o cargue un archivo para comenzar",
            style='Form.TLabel'
        )
        self.label_inicio.pack(pady=20)

    def mostrar_formulario_inicial(self):
        """Muestra el formulario completo para ingresar parámetros"""
        self._limpiar_formulario()
        
        parametros = ["Grupos", "Aulas", "Horarios"]  # Eliminé "Pisos" ya que está incluido en Aulas
        
        # Frame para parámetros
        param_frame = ttk.LabelFrame(
            self.frame,
            text="Configuración Inicial",
            padding=(10, 5)
        )
        param_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        # Crear campos de entrada
        for i, param in enumerate(parametros):
            self._crear_campo(param_frame, param, 0, i)

        # Botón de acción
        ttk.Button(
            self.frame,
            text="Generar Tablas",
            style='Accent.TButton',
            command=self._procesar_parametros
        ).grid(row=1, column=0, columnspan=3, pady=15, sticky="ew")

    def _crear_campo(self, parent, texto, fila, columna):
        """Crea un campo de entrada con su etiqueta"""
        ttk.Label(
            parent,
            text=f"{texto}:",
            style='Form.TLabel'
        ).grid(row=fila, column=columna, padx=5, pady=2, sticky="w")
        
        entry = ttk.Entry(
            parent,
            width=8,
            style='Form.TEntry'
        )
        entry.grid(row=fila+1, column=columna, padx=5, pady=2, sticky="ew")
        
        self.entradas[texto.lower()] = entry

    def _procesar_parametros(self):
        """Valida y procesa los parámetros ingresados"""
        try:
            params = {
                'grupos': self._validar_entero_positivo('grupos'),
                'aulas': self._validar_entero_positivo('aulas'),
                'horarios': self._validar_entero_positivo('horarios')
            }
            
            self.controller.generar_tablas(params)
            
        except ValueError as e:
            messagebox.showerror(
                "Error de Validación",
                str(e),
                parent=self.parent
            )

    def _validar_entero_positivo(self, clave):
        """Valida que el valor sea un entero positivo"""
        valor = self.entradas[clave].get().strip()
        
        if not valor:
            raise ValueError(f"El campo {clave.capitalize()} no puede estar vacío")
        
        try:
            num = int(valor)
            if num <= 0:
                raise ValueError(f"El número de {clave} debe ser mayor a cero")
            return num
        except ValueError:
            raise ValueError(f"Valor inválido para {clave.capitalize()}. Debe ser un número entero")

    def _limpiar_formulario(self):
        """Limpia y reinicia el formulario"""
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.entradas.clear()

    def pack(self, **kwargs):
        """Muestra el formulario usando pack"""
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        """Muestra el formulario usando grid"""
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        """Muestra el formulario usando place"""
        self.frame.place(**kwargs)