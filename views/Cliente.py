import flet as ft
import asyncio
from logic.gestor_clientes import registrar_cliente

def cliente_view(page: ft.Page, volver):

    nombre = ft.TextField(label="Nombre completo", expand=True)
    edad = ft.TextField(label="Edad", width=150, keyboard_type=ft.KeyboardType.NUMBER)

    sexo = ft.Dropdown(
        label="Sexo",
        width=200,
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino"),
            ft.dropdown.Option("Otro"),
        ]
    )

    fecha_nacimiento = ft.TextField(
        label="Fecha de nacimiento",
        hint_text="DD/MM/AAAA",
        read_only=True,
        expand=True
    )

    def seleccionar_fecha(e):
        date_picker.open = True
        page.update()

    def cambiar_fecha(e):
        fecha_nacimiento.value = str(date_picker.value.date())
        page.update()

    date_picker = ft.DatePicker(on_change=cambiar_fecha)
    page.overlay.append(date_picker)

    btn_fecha = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=seleccionar_fecha
    )

    def guardar(e):
        if not nombre.value or not edad.value or not sexo.value or not fecha_nacimiento:
            mensaje.value = "Por favor, completar todos los campos"
            mensaje.color = "red"
        else:
            exito, msj_res = registrar_cliente(
                nombre.value,
                edad.value,
                sexo.value,
                fecha_nacimiento.value
            )

            mensaje.value = msj_res

            if exito:
                mensaje.color = "green"
                nombre.value=""
                edad.value=""
                sexo.value=None
                fecha_nacimiento.value=""
            else:
                mensaje.color = "red"

        page.update()
        page.run_task(limpiar)

    mensaje = ft.Text()

    async def limpiar():
        await asyncio.sleep(2)
        mensaje.value = ""
        page.update()

    return ft.View(
        route="/cliente",
        controls=[
            ft.Column(
                [
                    ft.Text("Registro de Cliente", size=25, weight="bold"),
                    ft.Divider(),
                    nombre,
                    ft.Row([edad, sexo]),
                    ft.Row([fecha_nacimiento, btn_fecha]),
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", on_click=guardar),
                            ft.ElevatedButton("Volver", on_click=volver)
                        ]
                    ),
                    mensaje
                ],
                spacing=15
            )
        ]
    )