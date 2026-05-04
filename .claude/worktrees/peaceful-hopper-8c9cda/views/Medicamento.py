import flet as ft
import asyncio
from datetime import datetime
from database.conexion import conectar
from logic.gestor_medicamento import registrar_medicamento

def medicamento_view(page: ft.Page, volver):

    def guardar_m(e):
        data = {
            "nombre": nombre.value.strip(),
            "clasificacion": clasificacion.value,
            "presentacion": presentacion.value,
            "precio": float(precio.value) if precio.value else 0.0,
            "stock": int(stock.value) if stock.value else 0,
            "lote": lote.value.strip(),
            "precio_lote": float(precio_lote.value) if precio_lote.value else 0.0,
            "mg": int(mg.value) if mg.value else 0,
            "caducidad": caducidad.value,
            "fecha_alta": fecha_alta.value,
            "farmaceutica": farmaceutica.value.strip() if farmaceutica.value else "",
            "descripcion": descripcion.value.strip() if descripcion.value else ""

        }
        ok, msg = registrar_medicamento(data)
        if ok:
            mensaje.value = msg
            mensaje.color = "green"
            limpiar_campos()
        else:
            mensaje.value = f"Error: {msg}"
            mensaje.color = "red"

        page.update()
        limpiar_campos()
        
    nombre = ft.TextField(label="Nombre del Producto", expand=True)

    clasificacion = ft.Dropdown(
        label="Clasificación",
        expand=True,
        options=[
            ft.dropdown.Option("Analgésico"),
            ft.dropdown.Option("Antibiótico"),
            ft.dropdown.Option("Antiinflamatorio"),
            ft.dropdown.Option("Antialérgico"),
        ]
    )

    presentacion = ft.Dropdown(
        label="Presentación",
        expand=True,
        options=[
            ft.dropdown.Option("Tabletas"),
            ft.dropdown.Option("Jarabe"),
            ft.dropdown.Option("Cápsulas"),
            ft.dropdown.Option("Inyección"),
        ]
    )

    precio = ft.TextField(
        label="Precio Unitario",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    stock = ft.TextField(
        label="Stock",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    lote = ft.TextField(
        label="Número de lote",
        expand=True
    )

    precio_lote = ft.TextField(
        label="Precio por lote",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    mg = ft.TextField(
        label="Cantidad mg",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    caducidad = ft.TextField(
        label="Fecha de caducidad",
        read_only=True,
        expand=True
    )

    fecha_alta = ft.TextField(
        label="Fecha de alta",
        value=datetime.now().strftime("%Y-%m-%d"),
        read_only=True,
        expand=True
    )

    farmaceutica = ft.TextField(
        label="Farmacéutica",
        expand=True
    )

    descripcion = ft.TextField(
        label="Descripción",
        multiline=True,
        min_lines=3,
        max_lines=5,
        expand=True
    )

    mensaje = ft.Text()

    async def limpiar_mensaje():
        await asyncio.sleep(3)
        mensaje.value = ""
        page.update()

    def limpiar_campos():
        nombre.value = ""
        clasificacion.value = None
        presentacion.value = None
        precio.value = ""
        stock.value = ""
        lote.value = ""
        precio_lote.value = ""
        mg.value = ""
        caducidad.value = ""
        fecha_alta.value = datetime.now().strftime("%Y-%m-%d")
        farmaceutica.value = ""
        descripcion.value = ""
        page.update()

    def seleccionar_fecha(e):
        date_picker.open = True
        page.update()

    def cambiar_fecha(e):
        if date_picker.value:
            caducidad.value = date_picker.value.strftime("%Y-%m-%d")
            page.update()

    date_picker = ft.DatePicker(on_change=cambiar_fecha)
    page.overlay.append(date_picker)

    btn_fecha = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        tooltip="Seleccionar fecha",
        on_click=seleccionar_fecha
    )

    def guardar(e):
        if not nombre.value:
            mensaje.value = "Ingresa el nombre del producto"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        if not clasificacion.value:
            mensaje.value = "Selecciona la clasificación"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        if not presentacion.value:
            mensaje.value = "Selecciona la presentación"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        if not precio.value or not stock.value or not mg.value:
            mensaje.value = "Completa los campos numéricos"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        if not lote.value:
            mensaje.value = "Ingresa el número de lote"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        if not caducidad.value:
            mensaje.value = "Selecciona la fecha de caducidad"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        if not farmaceutica.value:
            mensaje.value = "Ingresa la farmacéutica"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

        try:
            precio_val = float(precio.value)
            stock_val = int(stock.value)
            mg_val = int(mg.value)
            precio_lote_val = float(precio_lote.value) if precio_lote.value else 0.0

        except ValueError:
            mensaje.value = "Datos numéricos inválidos"
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return

    btn_guardar = ft.ElevatedButton("Guardar", on_click=guardar_m)

    return ft.View(
        route="/medicamento",
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                padding=25,
                                width=800,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Alta de medicamento", size=24, weight=ft.FontWeight.BOLD),

                                        ft.Row([nombre]),
                                        ft.Row([clasificacion, presentacion]),
                                        ft.Row([precio, stock]),
                                        ft.Row([lote, precio_lote, mg]),
                                        ft.Row([caducidad, btn_fecha]),
                                        ft.Row([fecha_alta]),
                                        ft.Row([farmaceutica]),
                                        descripcion,

                                        ft.Row(
                                            [
                                                btn_guardar,
                                                ft.ElevatedButton("Volver", on_click=volver)
                                            ],
                                            alignment=ft.MainAxisAlignment.END
                                        ),

                                        mensaje
                                    ],
                                    scroll=ft.ScrollMode.AUTO
                                )
                            )
                        )
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )