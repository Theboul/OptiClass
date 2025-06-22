
def validate_positive_integer(value: str, field_name: str) -> int:
    """Valida que el valor sea un entero positivo"""
    try:
        num = int(value.strip())
        if num <= 0:
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número entero positivo.")

def validate_non_negative_integer(value: str, field_name: str) -> int:
    """Valida que el valor sea un entero no negativo"""
    try:
        num = int(value.strip())
        if num < 0:
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número entero no negativo.")

def validate_positive_float(value: str, field_name: str) -> float:
    """Valida que el valor sea un decimal positivo"""
    try:
        num = float(value.strip())
        if num <= 0:
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número decimal positivo.")

def validate_float_between_0_and_1(value: str, field_name: str) -> float:
    """Valida que el valor sea un decimal entre 0 y 1"""
    try:
        num = float(value.strip())
        if not (0 < num < 1):
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número decimal entre 0 y 1 (excluyendo los extremos).")

def validate_non_empty_text(value: str, field_name: str) -> str:
    """Valida que el texto no esté vacío"""
    if not value or not value.strip():
        raise ValueError(f"{field_name} no puede estar vacío.")
    return value.strip()
