# database/consultas.py
from database.conexion import conectar

# HELPERS INTERNOS


def _ejecutar_sp_lectura(nombre_sp, params=()):
    """Ejecuta un SP de lectura y devuelve lista de dicts."""
    conexion = conectar()
    if conexion is None:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.callproc(nombre_sp, params)
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        return resultados
    except Exception as e:
        print(f"Error en SP {nombre_sp}: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def _ejecutar_sp_escritura(nombre_sp, params=()):
    """Ejecuta un SP de escritura y hace commit."""
    conexion = conectar()
    if conexion is None:
        return False
    try:
        cursor = conexion.cursor()
        cursor.callproc(nombre_sp, params)
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error en SP {nombre_sp}: {e}")
        return False
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


# CLIENTES

def insertar_cliente(nombre, ap_paterno, ap_materno, edad, sexo, fecha_nacimiento,
                     peso, talla, oxigenacion, presion, temperatura, correo):
    return _ejecutar_sp_escritura(
        'sp_insertar_cliente',
        (nombre, ap_paterno, ap_materno, edad, sexo, fecha_nacimiento,
         peso, talla, oxigenacion, presion, temperatura, correo)
    )


def obtener_todos_clientes():
    return _ejecutar_sp_lectura('sp_obtener_todos_clientes')


def buscar_clientes_por_apellido(termino):
    return _ejecutar_sp_lectura('sp_buscar_clientes_por_apellido', (termino,))


def actualizar_cliente_bd(id_cliente, nombre, ap_paterno, ap_materno, edad, sexo,
                          fecha_nacimiento, peso, talla, oxigenacion,
                          presion, temperatura, correo):
    return _ejecutar_sp_escritura(
        'sp_actualizar_cliente',
        (id_cliente, nombre, ap_paterno, ap_materno, edad, sexo, fecha_nacimiento,
         peso, talla, oxigenacion, presion, temperatura, correo)
    )


def buscar_paciente_duplicado(nombre, ap_paterno, ap_materno, fecha_nacimiento):
    res = _ejecutar_sp_lectura(
        'sp_buscar_paciente_duplicado',
        (nombre, ap_paterno, ap_materno or '', fecha_nacimiento)
    )
    return res[0] if res else None


# MEDICAMENTOS

def insertar_medicamento(data):
    """Devuelve (exito, mensaje)."""
    conexion = conectar()
    if conexion is None:
        return False, "Error de conexión a la base de datos"
    try:
        cursor = conexion.cursor()
        valores = (
            data["nombre"], data["clasificacion"], data["presentacion"],
            data["precio"], data["stock"], data["lote"], data["precio_lote"],
            data["mg"], data["caducidad"], data["fecha_alta"],
            data["farmaceutica"], data["descripcion"]
        )
        cursor.callproc('sp_insertar_medicamento', valores)
        conexion.commit()
        return True, "Medicamento registrado exitosamente."
    except Exception as e:
        return False, str(e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def buscar_medicamentos_bd(termino):
    """Para venta/caja: devuelve tuplas (id, nombre, precio, stock)."""
    conexion = conectar()
    if conexion is None:
        return []
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_buscar_medicamentos', (termino,))
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        return resultados
    except Exception as e:
        print(f"Error al buscar medicamentos: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def buscar_farmaceuticas(termino):
    filas = _ejecutar_sp_lectura('sp_buscar_farmaceuticas', (termino,))
    return [fila['farmaceutica'] for fila in filas if fila.get('farmaceutica')]


def buscar_medicamento_existente(nombre, presentacion, cantidad_mg):
    res = _ejecutar_sp_lectura(
        'sp_buscar_medicamento_existente',
        (nombre, presentacion, cantidad_mg)
    )
    return res[0] if res else None


def reabastecer_medicamento(id_medicamento, stock_extra, nuevo_lote,
                            precio_lote, caducidad, precio_unitario):
    return _ejecutar_sp_escritura(
        'sp_reabastecer_medicamento',
        (id_medicamento, stock_extra, nuevo_lote, precio_lote,
         caducidad, precio_unitario)
    )


# --- NUEVAS funciones para autocompletado / tabla / edición ---

def autocompletar_medicamentos(termino):
    """SP: sp_autocompletar_medicamentos - sugerencias mientras escribes."""
    return _ejecutar_sp_lectura('sp_autocompletar_medicamentos', (termino,))


def obtener_todos_medicamentos():
    """SP: sp_obtener_todos_medicamentos - para la tabla completa."""
    return _ejecutar_sp_lectura('sp_obtener_todos_medicamentos')


def filtrar_medicamentos_por_clasificacion(clasificacion):
    """SP: sp_filtrar_medicamentos_clasificacion"""
    return _ejecutar_sp_lectura(
        'sp_filtrar_medicamentos_clasificacion',
        (clasificacion,)
    )


def actualizar_medicamento(id_med, clasificacion, precio_unit, stock,
                           numero_lote, precio_lote, caducidad,
                           farmaceutica, descripcion):
    """SP: sp_actualizar_medicamento - edita campos no identitarios."""
    return _ejecutar_sp_escritura(
        'sp_actualizar_medicamento',
        (id_med, clasificacion, precio_unit, stock, numero_lote,
         precio_lote, caducidad, farmaceutica, descripcion)
    )


# VENTAS

def procesar_venta_completa(total, tipo_consulta, carrito):
    conexion = conectar()
    if conexion is None:
        return False, "Error de conexión"
    try:
        cursor = conexion.cursor()
        resultado_venta = cursor.callproc(
            'sp_crear_venta', (total, tipo_consulta, 0))
        id_nueva_venta = resultado_venta[2]
        for item in carrito:
            valores_detalle = (
                id_nueva_venta, item["id_medicamento"], item["cantidad"],
                item["precio"], item["subtotal"]
            )
            cursor.callproc('sp_insertar_detalle', valores_detalle)
        conexion.commit()
        return True, "Venta registrada y stock actualizado correctamente."
    except Exception as e:
        conexion.rollback()
        return False, f"Error al procesar la venta: {e}"
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


# TRABAJADORES

def insertar_trabajador(nombre, ap_paterno, ap_materno, fecha_nac, genero,
                        curp, rfc, direccion, telefono, correo,
                        puesto, cedula, turno, fecha_ingreso):
    return _ejecutar_sp_escritura(
        'sp_insertar_trabajador',
        (nombre, ap_paterno, ap_materno, fecha_nac, genero,
         curp, rfc, direccion, telefono, correo,
         puesto, cedula, turno, fecha_ingreso)
    )


def obtener_trabajadores():
    return _ejecutar_sp_lectura('sp_obtener_todos_trabajadores')


def actualizar_trabajador_bd(id_trabajador, nombre, ap_paterno, ap_materno,
                             fecha_nac, genero, curp, rfc, direccion,
                             telefono, correo, puesto, cedula, turno, fecha_ingreso):
    return _ejecutar_sp_escritura(
        'sp_actualizar_trabajador',
        (id_trabajador, nombre, ap_paterno, ap_materno, fecha_nac, genero,
         curp, rfc, direccion, telefono, correo,
         puesto, cedula, turno, fecha_ingreso)
    )


def obtener_medico_por_id(id_medico):
    resultados = _ejecutar_sp_lectura(
        'sp_obtener_trabajador_por_id', (id_medico,))
    return resultados[0] if resultados else None


def buscar_trabajador_por_curp_rfc(curp, rfc):
    res = _ejecutar_sp_lectura(
        'sp_buscar_trabajador_por_curp_rfc', (curp, rfc))
    return res[0] if res else None

# HISTORIAL MÉDICO


def guardar_historial_bd(id_cliente, id_medico, fecha, diagnostico, tratamiento):
    return _ejecutar_sp_escritura(
        'sp_insertar_historial',
        (id_cliente, id_medico, fecha, diagnostico, tratamiento)
    )


def obtener_historial_bd(id_cliente):
    return _ejecutar_sp_lectura('sp_obtener_historial_cliente', (id_cliente,))

# HABILITAR Y DESAHBILITAR TRABAJADORES
def obtener_trabajadores():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM trabajadores")
        datos = cursor.fetchall()

        cursor.close()
        conn.close()

        return datos

    except Exception as e:
        print("❌ Error obtener trabajadores:", e)
        return []


def deshabilitar_trabajador(id_trabajador, observacion):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE trabajadores
            SET estado = 'INACTIVO',
                observacion_salida = %s
            WHERE id_trabajador = %s
        """, (observacion, id_trabajador))

        conn.commit()

        print("✅ Trabajador deshabilitado")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print("❌ Error deshabilitar:", e)
        return False


def activar_trabajador(id_trabajador):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE trabajadores
            SET estado = 'ACTIVO',
                observacion_salida = NULL
            WHERE id_trabajador = %s
        """, (id_trabajador,))

        conn.commit()

        print("✅ Trabajador activado")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print("❌ Error activar:", e)
        return False