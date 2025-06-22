import tkinter as tk
from tkinter import ttk

class ScrollableTable:
    def __init__(self, parent, titulo, headers, num_filas, ancho_columnas=12):
        """
        Crea una tabla scrollable con título, encabezados y número de filas especificado.
        
        Args:
            parent: Widget padre donde se colocará la tabla
            titulo (str): Título que aparecerá sobre la tabla
            headers (list): Lista de strings con los nombres de las columnas
            num_filas (int): Número de filas de datos que tendrá la tabla
            ancho_columnas (int): Ancho en caracteres de cada columna (por defecto 12)
        """
        self.parent = parent
        self.headers = headers
        self.num_filas = num_filas
        self.ancho_columnas = ancho_columnas
        
        # Contenedor principal
        self.contenedor = ttk.Frame(self.parent)
        
        # Configurar título
        self._configurar_titulo(titulo)
        
        # Configurar área scrollable
        self._configurar_scrollable()
        
        # Crear estructura de la tabla
        self._crear_estructura_tabla()

    def _configurar_titulo(self, titulo):
        """Configura el título de la tabla"""
        ttk.Label(
            self.contenedor, 
            text=titulo,
            font=('Segoe UI', 10, 'bold')
        ).pack(pady=(0, 5))

    def _configurar_scrollable(self):
        """Configura el área scrollable con canvas y scrollbar"""
        # Canvas y Scrollbar
        self.canvas = tk.Canvas(
            self.contenedor, 
            height=300,
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.contenedor, 
            orient="vertical", 
            command=self.canvas.yview
        )
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Frame interno para los contenidos
        self.frame_scroll = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_scroll, anchor="nw")
        
        # Configurar evento de redimensionamiento
        self.frame_scroll.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def _crear_estructura_tabla(self):
        """Crea la estructura completa de la tabla con encabezados y campos"""
        # Crear encabezados
        for i, header in enumerate(self.headers):
            ttk.Label(
                self.frame_scroll, 
                text=header,
                font=('Segoe UI', 9, 'bold'),
                padding=(5, 2)
            ).grid(row=0, column=i, sticky="ew", padx=5, pady=5)
        
        # Crear entradas de datos
        self.entradas = []
        for i in range(self.num_filas):
            fila = []
            for j in range(len(self.headers)):
                e = ttk.Entry(
                    self.frame_scroll, 
                    width=self.ancho_columnas,
                    font=('Segoe UI', 9)
                )
                e.grid(row=i+1, column=j, sticky="ew", padx=1, pady=1)
                fila.append(e)
            self.entradas.append(fila)
        
        # Configurar peso de columnas
        for i in range(len(self.headers)):
            self.frame_scroll.grid_columnconfigure(i, weight=1)

    def grid(self, **kwargs):
        """Coloca la tabla en el widget padre usando grid."""
        self.contenedor.grid(**kwargs)
    
    def pack(self, **kwargs):
        """Coloca la tabla en el widget padre usando pack."""
        self.contenedor.pack(**kwargs)
    
    def place(self, **kwargs):
        """Coloca la tabla en el widget padre usando place."""
        self.contenedor.place(**kwargs)

    def obtener_datos(self):
        """
        Obtiene todos los datos ingresados en la tabla.
        
        Returns:
            list: Lista de listas con los valores de cada fila
        """
        return [[e.get().strip() for e in fila] for fila in self.entradas]
    
    def limpiar(self):
        """Limpia todos los campos de entrada de la tabla."""
        for fila in self.entradas:
            for entrada in fila:
                entrada.delete(0, tk.END)
    
    def insertar_datos(self, datos):
        """
        Inserta datos en la tabla.
        
        Args:
            datos (list): Lista de listas con los valores a insertar en cada fila
            
        Raises:
            ValueError: Si los datos no coinciden con las dimensiones de la tabla
        """
        if len(datos) > len(self.entradas) or any(len(fila) > len(self.headers) for fila in datos):
            raise ValueError("Los datos exceden las dimensiones de la tabla")
            
        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                self.entradas[i][j].delete(0, tk.END)
                self.entradas[i][j].insert(0, str(valor))