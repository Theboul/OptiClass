#Constructor de la Clase Aula:

class Aula:
    def __init__(self, id_aula, capacidad, piso):
        if id_aula <= 0:
            raise ValueError("ID del aula debe ser psoitivo")
        if capacidad <= 0:
            raise ValueError("Capacidad del aula debe ser positiva")
        if piso < 0:
            raise ValueError("Piso del aula no puede ser negativo")
        
        self.id_aula = id_aula
        self.capacidad = capacidad
        self.piso = piso
    
    def __str__(self):
        return f"Aula(id={self.id_aula}, capacidad={self.capacidad}, piso={self.piso})"
