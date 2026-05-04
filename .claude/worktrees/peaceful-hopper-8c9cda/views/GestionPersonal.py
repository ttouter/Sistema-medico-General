import flet as ft
from database.consultas import obtener_trabajadores

def gestion_personal_view(page: ft.Page, ir_a_alta, ir_a_editar, volver):
    
    lista_empleados = obtener_trabajadores()
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Puesto")),
            ft.DataColumn(ft.Text("Turno")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(e['id_trabajador']))),
                    ft.DataCell(ft.Text(f"{e['nombre']} {e['ap_paterno']}")),
                    ft.DataCell(ft.Text(e['puesto'])),
                    ft.DataCell(ft.Text(e['turno'])),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            on_click=lambda _, emp=e: ir_a_editar(emp)
                        )
                    ),
                ]
            ) for e in lista_empleados
        ]
    )

    return ft.View(
        route="/gestion_personal",
        controls=[
            ft.Row([
                ft.Text("Gestión de Personal", size=30, weight="bold"),
                ft.Button("Nuevo Trabajador", icon=ft.Icons.ADD, on_click=ir_a_alta)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Column([tabla], scroll=ft.ScrollMode.AUTO, expand=True),
            ft.ElevatedButton("Volver al Menú", on_click=volver)
        ]
    )