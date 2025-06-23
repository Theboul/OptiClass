# === Clase Aula ===
class Aula:
    #Constructor de la Clase Aula: Representa un aula con ID, capacidad y piso.
    def __init__(self, id_aula: int, capacidad: int, piso: int):
        if not isinstance(id_aula, int) or id_aula <= 0:
            raise ValueError("ID del aula debe ser un entero positivo.")
        
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("Capacidad del aula debe ser un entero positivo.")
        
        if not isinstance(piso, int) or piso < 0:
            raise ValueError("Piso del aula debe ser un entero no negativo.")
        
        self._id_aula = id_aula
        self._capacidad = capacidad
        self._piso = piso
    
    @property
    def id_aula(self) -> int:
        return self._id_aula

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def piso(self) -> int:
        return self._piso
    
    def __str__(self):
        return f"Aula(id={self.id_aula}, capacidad={self.capacidad}, piso={self.piso})"
    

    #Permite crear una instancia desde un diccionario: Constructor para la carga de datos mediante JSON
    @classmethod
    def from_dict(cls, data: dict) -> 'Aula':
        return cls(
            id_aula=data['id_aula'],
            capacidad=data['capacidad'],
            piso=data['piso']
        )
    
    def to_dict(self):
        return {
            "id_aula": self.id_aula,
            "capacidad": self.capacidad,
            "piso": self.piso
        }

