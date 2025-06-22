import tkinter as tk

class AppMenuBar:
    def __init__(self, root, controller):
        """
        Inicializa la barra de menú conectada al controlador principal.
        
        Args:
            root: Ventana principal (tk.Tk)
            controller: Instancia del controlador principal (MainWindow)
        """
        self.root = root
        self.controller = controller
        self.menu_principal = tk.Menu(self.root)
        self.root.config(menu=self.menu_principal)
        self._crear_menu()

    def _crear_menu(self):
        """Crea la estructura del menú con todas sus opciones."""
        archivo_menu = tk.Menu(self.menu_principal, tearoff=0)
        
        # Opciones principales
        archivo_menu.add_command(
            label="Nuevo",
            command=self.controller.new_form
        )
        archivo_menu.add_command(
            label="Cargar Archivo JSON",
            command=self.controller.file_dialogs.cargar_json
        )
        archivo_menu.add_command(
            label="Guardar Archivo JSON",
            command=lambda: self.controller.file_dialogs.guardar_json(self.controller.parametros)
        )
        archivo_menu.add_command(
            label="Cargar Archivo CSV",
            command=self.controller.file_dialogs.cargar_csv
        )
        archivo_menu.add_command(
            label="Guardar Archivo CSV",
            command=lambda: self.controller.file_dialogs.guardar_csv(
                getattr(self.controller, 'resultado', None)
            )
        )
        
        archivo_menu.add_separator()

        # Opción condicional para ver resultados
        if hasattr(self.controller, 'results_dialog'):
            archivo_menu.add_command(
                label="Ver Resultados",
                command=lambda: self.controller.results_dialog.mostrar_resultados_detallados(
                    getattr(self.controller, 'resultado', None)
                )
            )
        
        archivo_menu.add_separator()

        # Salir de la aplicación
        archivo_menu.add_command(
            label="Salir",
            command=self.root.quit
        )

        self.menu_principal.add_cascade(
            label="Archivo",
            menu=archivo_menu
        )