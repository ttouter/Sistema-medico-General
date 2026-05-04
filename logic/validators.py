import re

RE_SOLO_LETRAS       = re.compile(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]")
RE_SOLO_NUMEROS      = re.compile(r"[^0-9]")
RE_NUMEROS_DECIMAL   = re.compile(r"[^0-9.]")
RE_LETRAS_NUMEROS    = re.compile(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s]")
RE_PRESION           = re.compile(r"[^0-9/]")
RE_LOTE              = re.compile(r"[^A-Za-z0-9-]")
RE_DOSIS             = re.compile(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s/().,-]")
RE_DIRECCION         = re.compile(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s,.#°-]")

RE_EMAIL             = re.compile(r"^[\w\.\-+]+@[\w\-]+\.[\w\.\-]+$")
RE_CURP              = re.compile(r"^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$")
RE_RFC_FISICA        = re.compile(r"^[A-ZÑ&]{4}[0-9]{6}[A-Z0-9]{3}$")
RE_RFC_MORAL         = re.compile(r"^[A-ZÑ&]{3}[0-9]{6}[A-Z0-9]{3}$")


# Filtros en tiempo real
def filtrar_letras(texto: str) -> str:
    """Permite solo letras (con acentos y ñ) y espacios."""
    return RE_SOLO_LETRAS.sub("", texto or "")

def filtrar_numeros(texto: str) -> str:
    """Permite solo dígitos."""
    return RE_SOLO_NUMEROS.sub("", texto or "")

def filtrar_numeros_decimal(texto: str) -> str:
    """Permite dígitos y un solo punto decimal."""
    if not texto:
        return ""
    limpio = RE_NUMEROS_DECIMAL.sub("", texto)
    # Permitir solo UN punto: si hay más, dejamos el primero
    if limpio.count(".") > 1:
        partes = limpio.split(".")
        limpio = partes[0] + "." + "".join(partes[1:])
    return limpio

def filtrar_letras_numeros(texto: str) -> str:
    """Permite letras, números y espacios."""
    return RE_LETRAS_NUMEROS.sub("", texto or "")

def filtrar_presion(texto: str) -> str:
    """Permite dígitos y la barra '/'. Ejemplo: 120/80"""
    return RE_PRESION.sub("", texto or "")

def filtrar_lote(texto: str) -> str:
    """Permite letras, números y guion. Ejemplo: L-001"""
    return RE_LOTE.sub("", (texto or "").upper())

def filtrar_dosis(texto: str) -> str:
    """Permite letras, números, espacios y signos comunes en dosis."""
    return RE_DOSIS.sub("", texto or "")

def filtrar_direccion(texto: str) -> str:
    """Permite letras, números, espacios y signos comunes en direcciones."""
    return RE_DIRECCION.sub("", texto or "")

def filtrar_curp(texto: str) -> str:
    """CURP: siempre mayúsculas, sin espacios, máx 18 caracteres."""
    return re.sub(r"[^A-Z0-9]", "", (texto or "").upper())[:18]

def filtrar_rfc(texto: str) -> str:
    """RFC: siempre mayúsculas, sin espacios, máx 13 caracteres."""
    return re.sub(r"[^A-ZÑ&0-9]", "", (texto or "").upper())[:13]


# Validaciones finales
def validar_nombre(valor, nombre_campo="Nombre", min_len=2):
    valor = (valor or "").strip()
    if not valor:
        return False, f"{nombre_campo} es obligatorio."
    if len(valor) < min_len:
        return False, f"{nombre_campo} debe tener al menos {min_len} caracteres."
    if RE_SOLO_LETRAS.search(valor):
        return False, f"{nombre_campo} solo puede contener letras."
    return True, ""

def validar_entero(valor, nombre_campo="Campo", min_val=None, max_val=None):
    if valor is None or str(valor).strip() == "":
        return False, f"{nombre_campo} es obligatorio."
    try:
        n = int(str(valor).strip())
    except ValueError:
        return False, f"{nombre_campo} debe ser un número entero."
    if min_val is not None and n < min_val:
        return False, f"{nombre_campo} debe ser mayor o igual a {min_val}."
    if max_val is not None and n > max_val:
        return False, f"{nombre_campo} debe ser menor o igual a {max_val}."
    return True, ""

def validar_decimal(valor, nombre_campo="Campo", min_val=None, max_val=None, opcional=False):
    s = str(valor or "").strip()
    if not s:
        if opcional:
            return True, ""
        return False, f"{nombre_campo} es obligatorio."
    try:
        n = float(s)
    except ValueError:
        return False, f"{nombre_campo} debe ser un número."
    if min_val is not None and n < min_val:
        return False, f"{nombre_campo} debe ser mayor o igual a {min_val}."
    if max_val is not None and n > max_val:
        return False, f"{nombre_campo} debe ser menor o igual a {max_val}."
    return True, ""

def validar_email(valor, opcional=True):
    s = (valor or "").strip()
    if not s:
        return (True, "") if opcional else (False, "Correo es obligatorio.")
    if not RE_EMAIL.match(s):
        return False, "Formato de correo inválido (ej: nombre@dominio.com)."
    return True, ""

def validar_telefono(valor, opcional=True, longitud=10):
    s = (valor or "").strip()
    if not s:
        return (True, "") if opcional else (False, "Teléfono es obligatorio.")
    if not s.isdigit():
        return False, "Teléfono solo debe contener números."
    if len(s) != longitud:
        return False, f"Teléfono debe tener exactamente {longitud} dígitos."
    return True, ""

def validar_curp(valor):
    s = (valor or "").strip().upper()
    if len(s) != 18:
        return False, "CURP debe tener exactamente 18 caracteres."
    if not RE_CURP.match(s):
        return False, "CURP no tiene formato válido."
    return True, ""

def validar_rfc(valor):
    s = (valor or "").strip().upper()
    if len(s) not in (12, 13):
        return False, "RFC debe tener 12 o 13 caracteres."
    if len(s) == 13 and not RE_RFC_FISICA.match(s):
        return False, "RFC de persona física no tiene formato válido."
    if len(s) == 12 and not RE_RFC_MORAL.match(s):
        return False, "RFC de persona moral no tiene formato válido."
    return True, ""

def validar_presion(valor, opcional=True):
    s = (valor or "").strip()
    if not s:
        return (True, "") if opcional else (False, "Presión es obligatoria.")
    if not re.match(r"^\d{2,3}/\d{2,3}$", s):
        return False, "Presión debe tener formato 120/80."
    return True, ""

def validar_cedula_profesional(valor, requerida=False):
    s = (valor or "").strip()
    if not s:
        return (True, "") if not requerida else (False, "Cédula profesional es obligatoria.")
    if not s.isdigit():
        return False, "Cédula solo debe contener números."
    if not (7 <= len(s) <= 8):
        return False, "Cédula debe tener entre 7 y 8 dígitos."
    return True, ""

def validar_fecha(valor, nombre_campo="Fecha"):
    s = (valor or "").strip()
    if not s:
        return False, f"{nombre_campo} es obligatoria."
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return False, f"{nombre_campo} debe tener formato AAAA-MM-DD."
    return True, ""


# Efectos para flet
def aplicar_error(textfield, mensaje):
    """Marca un TextField como inválido (borde rojo + helper text rojo)."""
    textfield.error_text = mensaje
    textfield.border_color = "red"

def limpiar_error(textfield):
    """Quita el estado de error del TextField."""
    textfield.error_text = None
    textfield.border_color = None