# logic/gestor_trabajadores.py
from database.consultas import insertar_trabajador, actualizar_trabajador_bd

# ==========================================
# FUNCIÓN 1: REGISTRAR (NUEVO TRABAJADOR)
# ==========================================
def registrar_trabajador(nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc, direccion, telefono, correo, puesto, cedula, turno, fecha_ingreso):
    """
    Validaciones básicas para el trabajador y envío a la base de datos (Insertar).
    """
    # 1. Limpieza de datos
    nombre = nombre.strip()
    curp = curp.strip().upper()
    rfc = rfc.strip().upper()
    
    # 2. Validaciones básicas
    if len(nombre) < 3:
        return False, "El nombre es demasiado corto."
    if len(curp) != 18:
        return False, "La CURP debe tener exactamente 18 caracteres."
    if len(rfc) < 12 or len(rfc) > 13:
        return False, "El RFC debe tener 12 o 13 caracteres."
        
    # Validar que si es Médico, traiga cédula
    if puesto == "Médico General" and not cedula.strip():
         return False, "Los médicos deben incluir su cédula profesional."

    # 3. Interacción con Base de Datos
    exito = insertar_trabajador(
        nombre, ap_paterno, ap_materno, fecha_nac, genero, 
        curp, rfc, direccion, telefono, correo, 
        puesto, cedula, turno, fecha_ingreso
    )
    
    if exito:
        return True, "Trabajador registrado exitosamente."
    else:
        return False, "Error al guardar el trabajador. Verifica que la CURP o RFC no estén duplicados."


# ==========================================
# FUNCIÓN 2: ACTUALIZAR (EDITAR TRABAJADOR)
# ==========================================
def actualizar_trabajador(id_trabajador, nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc, direccion, telefono, correo, puesto, cedula, turno, fecha_ingreso):
    """
    Valida y envía la actualización a la base de datos (Update).
    """
    # 1. Limpieza
    nombre = nombre.strip()
    curp = curp.strip().upper()
    rfc = rfc.strip().upper()
    
    # 2. Validaciones básicas
    if len(nombre) < 3:
        return False, "El nombre es demasiado corto."
    if len(curp) != 18:
        return False, "La CURP debe tener exactamente 18 caracteres."
        
    # Validar que si es Médico, traiga cédula
    if puesto == "Médico General" and not cedula.strip():
         return False, "Los médicos deben incluir su cédula profesional."
         
    # 3. Enviar a BD
    exito = actualizar_trabajador_bd(
        id_trabajador, nombre, ap_paterno, ap_materno, fecha_nac, genero, 
        curp, rfc, direccion, telefono, correo, 
        puesto, cedula, turno, fecha_ingreso
    )
    
    if exito:
        return True, "Trabajador actualizado exitosamente."
    else:
        return False, "Error al actualizar. Verifica que la CURP o RFC no estén duplicados."