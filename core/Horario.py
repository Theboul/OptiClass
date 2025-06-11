import re

class Horario:
    #Constructor de la Clase Horario:
    def __init__(self, id_horario: int, bloque: str):
        if not isinstance(id_horario, int) or id_horario <= 0:
            raise ValueError("ID del horario debe ser un entero positivo.")
        
        if not bloque or not bloque.strip():
            raise ValueError("Bloque horario no puede ser nulo o vacío.")
        
        # Validar formato HH:MM–HH:MM
        if not re.match(r"^\d{2}:\d{2}-\d{2}:\d{2}$", bloque.strip()):
            raise ValueError("Formato de horario inválido. Debe ser 'HH:MM-HH:MM' (ej: '07:00-09:15').")
        self._id_horario = id_horario
        self._bloque = bloque.strip()
    
    @property
    def id_horario(self) -> int:
        return self._id_horario

    @property
    def bloque(self) -> str:
        return self._bloque

    def __str__(self):
        return f"Horario(id={self.id_horario}, bloque='{self.bloque}')"
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Horario':
        return cls(
            id_horario=data['id_horario'],
            bloque=data['bloque']
        )
    
    def to_dict(self):
        return {
            "id_horario": self.id_horario,
            "bloque": self.bloque
        }
