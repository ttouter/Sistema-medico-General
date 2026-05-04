# logic/gestor_clientes.py
from database.consultas import (
    insertar_cliente,
    actualizar_cliente_bd,
    buscar_paciente_duplicado,
)
from logic.validators import (
    validar_nombre, validar_entero, validar_decimal,
    validar_email, validar_presion, validar_fecha,
)

class _ResultadoCliente(tuple):
    """
    Compatible con desempaque de 2 o 3 valores.
    """
    def __new__(cls, exito, mensaje, extra=None):
        return super().__new__(cls, (exito, mensaje, extra))

    def __iter__(self):
        # Por defecto desempaca 2 (compatibilidad con código viejo)
        return iter((self[0], self[1]))

    @property
    def exito(self):    return self[0]
    @property
    def mensaje(self):  return self[1]
    @property
    def extra(self):    return self[2]


def _validar_campos_paciente(nombre, ap_paterno, ap_materno, edad, sexo,
                             fecha_nacimiento, peso, talla, oxigenacion,
                             presion, temperatura, correo):
    """Validaciones comunes para alta y edición."""

    ok, msg = validar_nombre(nombre, "Nombre")
    if not ok: return False, msg

    ok, msg = validar_nombre(ap_paterno, "Apellido paterno")
    if not ok: return False, msg

    if ap_materno:
        ok, msg = validar_nombre(ap_materno, "Apellido materno")
        if not ok: return False, msg

    if not sexo:
        return False, "Sexo es obligatorio."

    ok, msg = validar_fecha(fecha_nacimiento, "Fecha de nacimiento")
    if not ok: return False, msg

    ok, msg = validar_entero(edad, "Edad", min_val=1, max_val=120)
    if not ok: return False, msg

    ok, msg = validar_decimal(peso, "Peso", min_val=0.5, max_val=300, opcional=True)
    if not ok: return False, msg

    ok, msg = validar_decimal(talla, "Talla", min_val=30, max_val=250, opcional=True)
    if not ok: return False, msg

    ok, msg = validar_decimal(oxigenacion, "Oxigenación", min_val=0, max_val=100, opcional=True)
    if not ok: return False, msg

    ok, msg = validar_presion(presion, opcional=True)
    if not ok: return False, msg

    ok, msg = validar_decimal(temperatura, "Temperatura", min_val=30, max_val=45, opcional=True)
    if not ok: return False, msg

    ok, msg = validar_email(correo, opcional=True)
    if not ok: return False, msg

    return True, ""


def _normalizar(nombre, ap_paterno, ap_materno, edad, peso, talla,
                oxigenacion, presion, temperatura, correo):
    return {
        "nombre":      nombre.strip(),
        "ap_paterno":  ap_paterno.strip(),
        "ap_materno":  ap_materno.strip() if ap_materno else "",
        "edad":        int(edad),
        "peso":        float(peso) if peso else None,
        "talla":       float(talla) if talla else None,
        "oxigenacion": float(oxigenacion) if oxigenacion else None,
        "presion":     presion.strip() if presion else None,
        "temperatura": float(temperatura) if temperatura else None,
        "correo":      correo.strip() if correo else None,
    }


def registrar_cliente(nombre, ap_paterno, ap_materno, edad, sexo,
                      fecha_nacimiento, peso, talla, oxigenacion,
                      presion, temperatura, correo,
                      forzar_aunque_duplicado=False):
    """Registra un cliente nuevo. Detecta duplicados."""

    ok, msg = _validar_campos_paciente(
        nombre, ap_paterno, ap_materno, edad, sexo, fecha_nacimiento,
        peso, talla, oxigenacion, presion, temperatura, correo
    )
    if not ok:
        return _ResultadoCliente(False, msg, None)

    n = _normalizar(nombre, ap_paterno, ap_materno, edad, peso, talla,
                    oxigenacion, presion, temperatura, correo)

    if not forzar_aunque_duplicado:
        duplicado = buscar_paciente_duplicado(
            n["nombre"], n["ap_paterno"], n["ap_materno"], fecha_nacimiento
        )
        if duplicado:
            return _ResultadoCliente(False, "DUPLICADO", duplicado)

    exito = insertar_cliente(
        n["nombre"], n["ap_paterno"], n["ap_materno"],
        n["edad"], sexo, fecha_nacimiento,
        n["peso"], n["talla"], n["oxigenacion"],
        n["presion"], n["temperatura"], n["correo"]
    )

    if exito:
        return _ResultadoCliente(True, "Cliente registrado correctamente.", None)
    return _ResultadoCliente(False, "Error al guardar en la base de datos.", None)


def actualizar_cliente(id_cliente, nombre, ap_paterno, ap_materno, edad, sexo,
                      fecha_nacimiento, peso, talla, oxigenacion,
                      presion, temperatura, correo):
    """Actualiza un cliente existente."""
    ok, msg = _validar_campos_paciente(
        nombre, ap_paterno, ap_materno, edad, sexo, fecha_nacimiento,
        peso, talla, oxigenacion, presion, temperatura, correo
    )
    if not ok:
        return False, msg

    n = _normalizar(nombre, ap_paterno, ap_materno, edad, peso, talla,
                    oxigenacion, presion, temperatura, correo)

    exito = actualizar_cliente_bd(
        id_cliente,
        n["nombre"], n["ap_paterno"], n["ap_materno"],
        n["edad"], sexo, fecha_nacimiento,
        n["peso"], n["talla"], n["oxigenacion"],
        n["presion"], n["temperatura"], n["correo"]
    )

    if exito:
        return True, "Cliente actualizado correctamente."
    return False, "Error al actualizar en la base de datos."