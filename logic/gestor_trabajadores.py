# logic/gestor_trabajadores.py
from database.consultas import (
    insertar_trabajador,
    actualizar_trabajador_bd,
    buscar_trabajador_por_curp_rfc,
)
from logic.validators import (
    validar_nombre, validar_curp, validar_rfc,
    validar_telefono, validar_email, validar_fecha,
    validar_cedula_profesional,
)


def _validar_campos_trabajador(nombre, ap_paterno, ap_materno, fecha_nac, genero,
                              curp, rfc, telefono, correo, puesto, cedula,
                              turno, fecha_ingreso):
    """Validaciones comunes. Devuelve (ok, msg)."""

    ok, msg = validar_nombre(nombre, "Nombre", min_len=2)
    if not ok: return False, msg

    ok, msg = validar_nombre(ap_paterno, "Apellido paterno", min_len=2)
    if not ok: return False, msg

    if ap_materno:
        ok, msg = validar_nombre(ap_materno, "Apellido materno")
        if not ok: return False, msg

    if not genero:
        return False, "Género es obligatorio."

    ok, msg = validar_fecha(fecha_nac, "Fecha de nacimiento")
    if not ok: return False, msg

    ok, msg = validar_curp(curp)
    if not ok: return False, msg

    ok, msg = validar_rfc(rfc)
    if not ok: return False, msg

    ok, msg = validar_telefono(telefono, opcional=True, longitud=10)
    if not ok: return False, msg

    ok, msg = validar_email(correo, opcional=True)
    if not ok: return False, msg

    if not puesto:
        return False, "Puesto es obligatorio."

    if not turno:
        return False, "Turno es obligatorio."

    ok, msg = validar_fecha(fecha_ingreso, "Fecha de ingreso")
    if not ok: return False, msg

    # Cédula obligatoria solo para Médico General
    es_medico = (puesto == "Médico General")
    ok, msg = validar_cedula_profesional(cedula, requerida=es_medico)
    if not ok: return False, msg

    return True, ""


def registrar_trabajador(nombre, ap_paterno, ap_materno, fecha_nac, genero,
                        curp, rfc, direccion, telefono, correo, puesto,
                        cedula, turno, fecha_ingreso):
    """Inserta un trabajador nuevo. Verifica unicidad de CURP y RFC."""

    ok, msg = _validar_campos_trabajador(
        nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc,
        telefono, correo, puesto, cedula, turno, fecha_ingreso
    )
    if not ok:
        return False, msg

    curp_limpio = curp.strip().upper()
    rfc_limpio = rfc.strip().upper()

    # Verificar unicidad antes de intentar insertar
    duplicado = buscar_trabajador_por_curp_rfc(curp_limpio, rfc_limpio)
    if duplicado:
        if duplicado.get('curp') == curp_limpio:
            return False, f"Ya existe un trabajador con esa CURP ({duplicado['nombre']} {duplicado['ap_paterno']})."
        if duplicado.get('rfc') == rfc_limpio:
            return False, f"Ya existe un trabajador con ese RFC ({duplicado['nombre']} {duplicado['ap_paterno']})."

    # Cédula vacía si no es médico
    cedula_final = cedula.strip() if puesto == "Médico General" else ""

    exito = insertar_trabajador(
        nombre.strip(), ap_paterno.strip(), ap_materno.strip() if ap_materno else "",
        fecha_nac, genero, curp_limpio, rfc_limpio,
        direccion.strip() if direccion else "",
        telefono.strip() if telefono else "",
        correo.strip() if correo else "",
        puesto, cedula_final, turno, fecha_ingreso
    )

    if exito:
        return True, "Trabajador registrado exitosamente."
    return False, "Error al guardar el trabajador."


def actualizar_trabajador(id_trabajador, nombre, ap_paterno, ap_materno, fecha_nac,
                         genero, curp, rfc, direccion, telefono, correo,
                         puesto, cedula, turno, fecha_ingreso):
    """Actualiza un trabajador existente. Verifica que CURP/RFC no coincidan con OTRO."""

    ok, msg = _validar_campos_trabajador(
        nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc,
        telefono, correo, puesto, cedula, turno, fecha_ingreso
    )
    if not ok:
        return False, msg

    curp_limpio = curp.strip().upper()
    rfc_limpio = rfc.strip().upper()

    # Verificar unicidad: si la CURP/RFC pertenece a OTRO trabajador, no permitir
    duplicado = buscar_trabajador_por_curp_rfc(curp_limpio, rfc_limpio)
    if duplicado and duplicado.get('id_trabajador') != id_trabajador:
        if duplicado.get('curp') == curp_limpio:
            return False, f"Esa CURP ya pertenece a otro trabajador ({duplicado['nombre']} {duplicado['ap_paterno']})."
        if duplicado.get('rfc') == rfc_limpio:
            return False, f"Ese RFC ya pertenece a otro trabajador ({duplicado['nombre']} {duplicado['ap_paterno']})."

    cedula_final = cedula.strip() if puesto == "Médico General" else ""

    exito = actualizar_trabajador_bd(
        id_trabajador,
        nombre.strip(), ap_paterno.strip(), ap_materno.strip() if ap_materno else "",
        fecha_nac, genero, curp_limpio, rfc_limpio,
        direccion.strip() if direccion else "",
        telefono.strip() if telefono else "",
        correo.strip() if correo else "",
        puesto, cedula_final, turno, fecha_ingreso
    )

    if exito:
        return True, "Trabajador actualizado exitosamente."
    return False, "Error al actualizar."