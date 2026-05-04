import flet as ft
import asyncio
# Asegúrate de importar ambas funciones de tu capa lógica
from logic.gestor_trabajadores import registrar_trabajador, actualizar_trabajador

def alta_trabajadores_view(page: ft.Page, volver, datos_edicion=None):

    # 1. Definición de controles
    id_trabajador_field = ft.TextField(label="ID", read_only=True, width=100, hint_text="Auto", disabled=True)

    nombre = ft.TextField(label="Nombre(s)", expand=True)
    ap_paterno = ft.TextField(label="Apellido Paterno", expand=True)
    ap_materno = ft.TextField(label="Apellido Materno", expand=True)

    fecha_nac = ft.TextField(label="Fecha de Nacimiento", hint_text="AAAA-MM-DD", read_only=True)
    fecha_ingreso = ft.TextField(label="Fecha de Ingreso", hint_text="AAAA-MM-DD", read_only=True)

    # --- Lógica para Fecha de Nacimiento ---
    def cambiar_fecha_nac(e):
        if date_picker_nac.value:
            fecha_nac.value = date_picker_nac.value.strftime("%Y-%m-%d")
        page.update()

    date_picker_nac = ft.DatePicker(on_change=cambiar_fecha_nac)

    # --- Lógica para Fecha de Ingreso ---
    def cambiar_fecha_ingre(e):
        if date_picker_ingreso.value:
            fecha_ingreso.value = date_picker_ingreso.value.strftime("%Y-%m-%d")
        page.update()

    date_picker_ingreso = ft.DatePicker(on_change=cambiar_fecha_ingre)

    # Agregar ambos al overlay de la página
    page.overlay.extend([date_picker_nac, date_picker_ingreso])

    # Botones que abren sus respectivos selectores
    btn_fecha_nac = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: setattr(date_picker_nac, "open", True) or page.update()
    )

    btn_fecha_ingre = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: setattr(date_picker_ingreso, "open", True) or page.update()
    )

    genero = ft.Dropdown(
        label="Género",
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino"),
        ],
    )

    curp = ft.TextField(label="CURP")
    rfc = ft.TextField(label="RFC")
    direccion = ft.TextField(label="Dirección completa", multiline=True)
    telefono = ft.TextField(label="Teléfono")
    correo = ft.TextField(label="Correo electrónico")

    # Dropdown creado sin el evento adentro
    puesto = ft.Dropdown(
        label="Puesto",
        options=[
            ft.dropdown.Option("Médico General"),
            ft.dropdown.Option("Recepcionista"),
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Mantenimiento"),
        ],
    )

    cedula = ft.TextField(label="Cédula Profesional", disabled=True)

    def cambiar_puesto(e):
        if puesto.value == "Médico General":
            cedula.disabled = False
        else:
            cedula.disabled = True
            cedula.value = ""
        page.update()

    # Asignamos el evento DESPUÉS de crearlo
    puesto.on_change = cambiar_puesto

    turno = ft.Dropdown(
        label="Turno",
        options=[
            ft.dropdown.Option("Matutino"),
            ft.dropdown.Option("Vespertino"),
            ft.dropdown.Option("Nocturno"),
            ft.dropdown.Option("Mixto"),
        ],
    )

    mensaje = ft.Text()

    # =========================================================
    # 2. Llenar los campos si estamos en MODO EDICIÓN
    # =========================================================
    if datos_edicion:
        id_trabajador_field.value = str(datos_edicion.get('id_trabajador', ''))
        id_trabajador_field.disabled = False
        nombre.value = datos_edicion.get('nombre', '')
        ap_paterno.value = datos_edicion.get('ap_paterno', '')
        ap_materno.value = datos_edicion.get('ap_materno', '')
        fecha_nac.value = str(datos_edicion.get('fecha_nacimiento', ''))
        genero.value = datos_edicion.get('genero')
        curp.value = datos_edicion.get('curp', '')
        rfc.value = datos_edicion.get('rfc', '')
        direccion.value = datos_edicion.get('direccion', '')
        telefono.value = datos_edicion.get('telefono', '')
        correo.value = datos_edicion.get('correo', '')
        puesto.value = datos_edicion.get('puesto')
        cedula.value = datos_edicion.get('cedula_profesional', '')
        turno.value = datos_edicion.get('turno')
        fecha_ingreso.value = str(datos_edicion.get('fecha_ingreso', ''))
        
        # Validar si el puesto cargado es Médico General para habilitar la cédula
        if puesto.value == "Médico General":
            cedula.disabled = False

    # =========================================================
    # 3. Lógica para Guardar (Insertar o Actualizar)
    # =========================================================
    async def limpiar_mensaje():
        await asyncio.sleep(3)
        mensaje.value = ""
        page.update()

    def guardar(e):
        if not nombre.value or not ap_paterno.value or not fecha_nac.value or not genero.value or not curp.value or not rfc.value or not puesto.value or not turno.value:
            mensaje.value = "Por favor llena todos los campos obligatorios."
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        if datos_edicion:
            # MODO EDICIÓN: Llama a la función de actualizar
            exito, msj_res = actualizar_trabajador(
                datos_edicion['id_trabajador'], # Mandamos el ID para saber a quién actualizar
                nombre.value, ap_paterno.value, ap_materno.value, 
                fecha_nac.value, genero.value, curp.value, rfc.value, 
                direccion.value, telefono.value, correo.value, 
                puesto.value, cedula.value, turno.value, fecha_ingreso.value
            )
        else:
            # MODO NUEVO REGISTRO: Llama a la función de registrar
            exito, msj_res = registrar_trabajador(
                nombre.value, ap_paterno.value, ap_materno.value, 
                fecha_nac.value, genero.value, curp.value, rfc.value, 
                direccion.value, telefono.value, correo.value, 
                puesto.value, cedula.value, turno.value, fecha_ingreso.value
            )

        mensaje.value = msj_res
        if exito:
            mensaje.color = "green"
            if not datos_edicion:
                # Solo limpiamos las cajas de texto si era un registro NUEVO
                for campo in [nombre, ap_paterno, ap_materno, fecha_nac, curp, rfc, direccion, telefono, correo, cedula, fecha_ingreso]:
                    campo.value = ""
                puesto.value = None
                genero.value = None
                turno.value = None
        else:
            mensaje.color = "red"
            
        page.update()
        page.run_task(limpiar_mensaje)

    # Cambiar dinámicamente el título y el botón dependiendo del modo
    titulo_vista = "Editar Personal Médico" if datos_edicion else "Registro de Personal Médico"
    texto_boton = "Guardar Cambios" if datos_edicion else "Guardar"

    btn_guardar = ft.ElevatedButton(texto_boton, icon=ft.Icons.SAVE, on_click=guardar)

    return ft.View(
        route="/alta_trabajadores",
        controls=[
            ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Card(
                                    elevation=5,
                                    content=ft.Container(
                                        width=900,
                                        padding=25,
                                        content=ft.Column(
                                            [
                                                ft.Text(titulo_vista, size=26, weight="bold"),
                                                ft.Divider(),
                                                ft.Text("Datos Personales", weight="bold"),
                                                ft.Row([id_trabajador_field, nombre, ap_paterno, ap_materno]),
                                                ft.Row([fecha_nac, btn_fecha_nac, genero]),
                                                ft.Row([curp, rfc]),
                                                direccion,
                                                ft.Row([telefono, correo]),
                                                ft.Divider(),
                                                ft.Text("Datos Profesionales", weight="bold"),
                                                ft.Row([puesto, cedula]),
                                                ft.Row([turno, fecha_ingreso, btn_fecha_ingre]),
                                                ft.Row(
                                                    [
                                                        btn_guardar,
                                                        ft.ElevatedButton("Volver", on_click=volver)
                                                    ],
                                                    alignment=ft.MainAxisAlignment.END
                                                ),
                                                mensaje
                                            ],
                                            spacing=15
                                        )
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            )
        ]
    )