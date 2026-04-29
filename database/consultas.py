# database/consultas.py
from database.conexion import conectar

def insertar_cliente(nombre, edad, sexo, fecha_nacimiento):
    conexion = conectar()
    if conexion is None:
        return False
        
    try:
        cursor = conexion.cursor()
        
        # Parámetros en el mismo orden que pide el procedimiento almacenado
        valores = (nombre, edad, sexo, fecha_nacimiento)
        
        # Llamamos al procedimiento almacenado
        cursor.callproc('sp_insertar_cliente', valores)
        
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error en BD: {e}")
        return False
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def insertar_medicamento(data):
    conexion = conectar()
    if conexion is None:
        return False, "Error de conexión a la base de datos"
        
    try:
        cursor = conexion.cursor()
        
        # Preparamos los valores en el mismo orden que pide el procedimiento almacenado
        valores = (
            data["nombre"], 
            data["clasificacion"], 
            data["presentacion"],
            data["precio"], 
            data["stock"], 
            data["lote"],
            data["precio_lote"], 
            data["mg"], 
            data["caducidad"],
            data["fecha_alta"], 
            data["farmaceutica"], 
            data["descripcion"]
        )
        
        # Llamamos al procedimiento almacenado
        cursor.callproc('sp_insertar_medicamento', valores)
        
        conexion.commit()
        return True, "Medicamento registrado exitosamente."
        
    except Exception as e:
        # Aquí capturamos si hay un error, como un lote duplicado
        return False, str(e)
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def procesar_venta_completa(total, tipo_consulta, carrito):
    """
    carrito debe ser una lista de diccionarios, por ejemplo:
    [
        {"id_medicamento": 1, "cantidad": 2, "precio": 10.50, "subtotal": 21.00},
        {"id_medicamento": 5, "cantidad": 1, "precio": 25.00, "subtotal": 25.00}
    ]
    """
    conexion = conectar()
    if conexion is None:
        return False, "Error de conexión"
        
    try:
        cursor = conexion.cursor()
        
        # 1. Llamar al SP de la cabecera de la venta
        # El tercer parámetro es '0' porque es una variable OUT que MySQL va a llenar
        resultado_venta = cursor.callproc('sp_crear_venta', (total, tipo_consulta, 0))
        
        # El ID de la venta recién creada nos lo devuelve en la posición 2 (el tercer parámetro)
        id_nueva_venta = resultado_venta[2] 
        
        # 2. Recorrer el carrito y llamar al SP de detalles por cada producto
        for item in carrito:
            valores_detalle = (
                id_nueva_venta,
                item["id_medicamento"],
                item["cantidad"],
                item["precio"],
                item["subtotal"]
            )
            cursor.callproc('sp_insertar_detalle', valores_detalle)
            
        # 3. Si todo salió bien con la cabecera y todos los detalles, guardamos los cambios
        conexion.commit()
        return True, "Venta registrada y stock actualizado correctamente."
        
    except Exception as e:
        # Si algo falla (ej. no hay stock suficiente), revertimos todo para que no queden ventas a medias
        conexion.rollback() 
        return False, f"Error al procesar la venta: {e}"
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def buscar_medicamentos_bd(termino):
    conexion = conectar()
    if conexion is None:
        return []
        
    try:
        cursor = conexion.cursor()
        # Buscamos por nombre y nos traemos: ID, Nombre, Precio y Stock
        query = """
            SELECT id_medicamento, nombre_producto, precio_unitario, stock 
            FROM medicamentos 
            WHERE nombre_producto LIKE %s AND stock > 0 
            LIMIT 5
        """
        # El % alrededor del término permite buscar coincidencias parciales
        cursor.execute(query, (f"%{termino}%",)) 
        resultados = cursor.fetchall()
        return resultados
        
    except Exception as e:
        print(f"Error al buscar: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Agregar dentro de database/consultas.py
def insertar_trabajador(nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc, direccion, telefono, correo, puesto, cedula, turno, fecha_ingreso):
    conexion = conectar()
    if conexion is None:
        return False
        
    try:
        cursor = conexion.cursor()
        
        # Parámetros en el mismo orden que pide el procedimiento almacenado
        valores = (nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc, direccion, telefono, correo, puesto, cedula, turno, fecha_ingreso)
        
        # Llamamos al procedimiento almacenado
        cursor.callproc('sp_insertar_trabajador', valores)
        
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error en BD (Trabajadores): {e}")
        return False
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def obtener_trabajadores():
    # 1. Colocamos TODO el intento de conexión dentro del try
    try:
        from database.conexion import conectar
        conexion = conectar()
        
        if conexion is None: 
            return []
            
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM trabajadores")
        resultados = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return resultados
        
    except Exception as e:
        # 2. Si XAMPP está apagado, Python cae aquí en lugar de romper la app
        print(f"❌ Error de conexión al cargar trabajadores: {e}")
        return [] # Retornamos una lista vacía para que Flet pueda dibujar la tabla sin datos

# 👇 AGREGA ESTA NUEVA FUNCIÓN AL FINAL DE database/consultas.py

def actualizar_trabajador_bd(id_trabajador, nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc, direccion, telefono, correo, puesto, cedula, turno, fecha_ingreso):
    # Asume que tienes importado conectar() al inicio del archivo
    from database.conexion import conectar 
    
    conexion = conectar()
    if conexion is None:
        return False
        
    try:
        cursor = conexion.cursor()
        
        # Consulta SQL directa para actualizar todos los campos
        query = """
            UPDATE trabajadores 
            SET nombre=%s, ap_paterno=%s, ap_materno=%s, fecha_nacimiento=%s, 
                genero=%s, curp=%s, rfc=%s, direccion=%s, telefono=%s, 
                correo=%s, puesto=%s, cedula_profesional=%s, turno=%s, fecha_ingreso=%s
            WHERE id_trabajador=%s
        """
        
        # Los valores deben ir en el mismo orden que los %s de arriba
        valores = (nombre, ap_paterno, ap_materno, fecha_nac, genero, curp, rfc, direccion, 
                telefono, correo, puesto, cedula, turno, fecha_ingreso, id_trabajador)
        
        cursor.execute(query, valores)
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error en BD (Actualizar Trabajador): {e}")
        return False
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()