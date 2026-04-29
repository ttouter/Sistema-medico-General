import flet as ft
from views.Cliente import cliente_view
from views.Medicamento import medicamento_view
from views.RecetaCompleta import receta_completa_view
from views.Altatrabajadores import alta_trabajadores_view
from views.venta import caja_view
from views.GestionPersonal import gestion_personal_view

def main(page: ft.Page):
    page.title = "Dashboard"
    page.window.width = 950
    page.window.height = 600

    # ------------------ INICIO ------------------
    def cargar_inicio(e=None):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/dashboard",
                controls=[
                    header,
                    content
                ]
            )
        )
        page.update()

    # ------------------ Login ------------------    
    def cargar_login(e):
        page.views.clear()
        page.views.append(main(page, cargar_inicio))
        page.update()

    # ------------------ FUNCIONES ------------------
    def ir_cliente(e):
        page.views.clear()
        page.views.append(cliente_view(page, cargar_inicio))
        page.update()

    def ir_medicamento(e):
        page.views.clear()
        page.views.append(medicamento_view(page, cargar_inicio))
        page.update()
        
    def ir_receta_completa(e):
        page.views.clear()
        page.views.append(receta_completa_view(page, cargar_inicio))
        page.update()
    
    def ir_altaTra(e):
        page.views.clear()
        page.views.append(alta_trabajadores_view(page, ir_gestion_personal))
        page.update()

    def ir_venta(e):
        page.views.clear()
        page.views.append(caja_view(page, cargar_inicio))
        page.update()
    
    def ir_gestion_personal(e):
        page.views.clear()
        page.views.append(
            gestion_personal_view(
                page, 
                ir_a_alta=ir_altaTra, # Formulario vacío
                ir_a_editar=ir_editar_trabajador, # Formulario con datos
                volver=cargar_inicio
        )
    )
    page.update()

    def ir_editar_trabajador(datos_empleado):
        page.views.clear()
    # Pasamos los datos del empleado a la vista de Alta para que los cargue
        page.views.append(alta_trabajadores_view(page, ir_gestion_personal, datos_empleado))
        page.update()

    # ------------------ HEADER ------------------
    header = ft.Container(
        content=ft.Row(
            [
                ft.Text("MediLink", size=22, weight="bold"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.Padding.only(left=0, top=20, right=20, bottom=20)
    )

    # ------------------ BOTÓN ------------------
    btn1 = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.PERSON, size=40),
                ft.Text("Paciente")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        border_radius=10,
        ink=True,
        on_click=ir_cliente,
        width=150,
        height=120
    )
    
    btn2 = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.MEDICATION, size=40),
                ft.Text("Medicamentos")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        border_radius=10,
        ink=True,
        on_click=ir_medicamento,
        width=150,
        height=120
    )
    
    btn3 = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.RECEIPT_LONG, size=40),
                ft.Text("Receta Completa")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        border_radius=10,
        ink=True,
        on_click=ir_receta_completa,
        width=150,
        height=120
    )

    btn_4 = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.PERSON, size=40),
                ft.Text("Gestión de Personal")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        border_radius=10,
        ink=True,
        on_click=ir_gestion_personal,
        width=150,
        height=120
    )

    btn_5 = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.MONEY, size=40),
                ft.Text("Venta")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        border_radius=10,
        ink=True,
        on_click=ir_venta,
        width=150,
        height=120
    )

    content = ft.Column(
        [
            ft.Text("Panel principal", size=20),
            ft.Row([btn1, btn2, btn3, btn_4, btn_5], alignment=ft.MainAxisAlignment.CENTER, spacing=30)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    cargar_inicio()

ft.run(main)