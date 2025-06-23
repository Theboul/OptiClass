
def validate_positive_integer(value: str, field_name: str) -> int:
    """
    Valida que el valor proporcionado sea un número entero positivo (> 0).
    
    Parámetros:
    - value (str): El valor a validar, usualmente una cadena proveniente de una entrada de texto.
    - field_name (str): El nombre del campo (usado para mensajes de error).

    Retorna:
    - int: El número entero validado y convertido.

    Lanza:
    - ValueError: Si el valor no es un entero o si es menor o igual a cero.
    """
    try:
        num = int(value.strip())
        if num <= 0:
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número entero positivo.")

def validate_non_negative_integer(value: str, field_name: str) -> int:
    """
    Valida que el valor sea un número entero no negativo (>= 0).
    
    Parámetros:
    - value (str): Entrada de texto a verificar.
    - field_name (str): Nombre del campo para los mensajes de error.

    Retorna:
    - int: El número entero convertido.

    Lanza:
    - ValueError: Si el valor no es un entero o si es negativo.
    """
    try:
        num = int(value.strip())
        if num < 0:
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número entero no negativo.")

def validate_positive_float(value: str, field_name: str) -> float:
    """
    Valida que el valor sea un número decimal positivo (> 0).
    
    Parámetros:
    - value (str): Valor a convertir.
    - field_name (str): Campo asociado (para mensaje de error).

    Retorna:
    - float: Valor convertido y validado.

    Lanza:
    - ValueError: Si el valor no es un float o es negativo/cero.
    """
    try:
        num = float(value.strip())
        if num <= 0:
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número decimal positivo.")

def validate_float_between_0_and_1(value: str, field_name: str) -> float:
    """
    Valida que el valor sea un decimal estrictamente entre 0 y 1 (0 < x < 1).
    
    Parámetros:
    - value (str): Entrada de texto.
    - field_name (str): Nombre del campo.

    Retorna:
    - float: Valor convertido si es válido.

    Lanza:
    - ValueError: Si el valor no es float o está fuera del rango (0, 1).
    """
    try:
        num = float(value.strip())
        if not (0 < num < 1):
            raise ValueError
        return num
    except ValueError:
        raise ValueError(f"{field_name} debe ser un número decimal entre 0 y 1 (excluyendo los extremos).")

def validate_non_empty_text(value: str, field_name: str) -> str:
    """
    Valida que el texto no esté vacío o compuesto solo por espacios.

    Parámetros:
    - value (str): El texto a validar.
    - field_name (str): Nombre del campo a validar.

    Retorna:
    - str: El texto limpiado (sin espacios extra).

    Lanza:
    - ValueError: Si el texto está vacío o solo tiene espacios.
    """
    if not value or not value.strip():
        raise ValueError(f"{field_name} no puede estar vacío.")
    return value.strip()
