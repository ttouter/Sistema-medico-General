from database.consultas import insertar_medicamento

def registrar_medicamento(data):
    # Aquí puedes agregar validaciones adicionales como haces en clientes
    if not data["nombre"]:
        return False, "El nombre es obligatorio"
    
    # Si todo está bien, llamamos a la base de datos
    return insertar_medicamento(data)