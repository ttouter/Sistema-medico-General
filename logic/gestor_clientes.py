from database.consultas import insertar_cliente

def registrar_cliente(nombre, edad, sexo, fecha_nacimiento):
    """
    Recibe los datos de la vista, aplica reglas de negocio y los envía a la BD.
    Retorna: (bool: exito, str: mensaje)
    """
    
    # 1. Limpieza de datos (quitar espacios en blanco al inicio y final)
    nombre = nombre.strip()
    
    # 2. Validación de reglas de negocio
    # Verificar que la edad sea realmente un número y tenga sentido lógico
    try:
        edad_int = int(edad)
        if edad_int <= 0 or edad_int > 120:
            return False, "Por favor ingresa una edad válida (entre 1 y 120)."
    except ValueError:
        return False, "La edad debe ser un número entero."

    # Podrías agregar más validaciones aquí, por ejemplo:
    # - Que el nombre tenga al menos 3 caracteres
    if len(nombre) < 3:
        return False, "El nombre es demasiado corto."

    # 3. Interacción con la capa de Base de Datos
    # Si pasa todas las validaciones, mandamos a ejecutar el procedimiento almacenado
    exito = insertar_cliente(nombre, edad_int, sexo, fecha_nacimiento)
    
    # 4. Retornar la respuesta final a la vista
    if exito:
        return True, "Cliente registrado exitosamente."
    else:
        return False, "Error al guardar el registro en el sistema."