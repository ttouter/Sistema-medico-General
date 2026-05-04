import flet as ft
from database.consultas import (
    obtener_trabajadores,
    deshabilitar_trabajador,
    activar_trabajador
)


def gestion_personal_view(page: ft.Page, ir_a_alta, ir_a_editar, volver):

    lista_empleados = obtener_trabajadores()

    # ---------------- RECARGAR ----------------
    def recargar():
        page.views.clear()
        page.views.append(gestion_personal_view(page, ir_a_alta, ir_a_editar, volver))
        page.update()

    # ---------------- DESHABILITAR ----------------
    def confirmar_baja(emp):

        observacion = ft.TextField(label="Motivo de salida", multiline=True)

        def guardar_baja(e):
            if not observacion.value:
                observacion.error_text = "Campo obligatorio"
                page.update()
                return

            ok = deshabilitar_trabajador(emp['id_trabajador'], observacion.value)

            if ok:
                recargar()

        dialog = ft.AlertDialog(
            title=ft.Text("Deshabilitar trabajador"),
            content=observacion,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar()),
                ft.ElevatedButton("Guardar", on_click=guardar_baja)
            ]
        )

        def cerrar():
            dialog.open = False
            page.update()

        page.dialog = dialog
        dialog.open = True
        page.update()

    # ---------------- ACTIVAR ----------------
    def activar(emp):
        ok = activar_trabajador(emp['id_trabajador'])

        if ok:
            recargar()

    # ---------------- TABLA ----------------
    filas = []

    for e in lista_empleados:

        estado = e.get('estado', 'ACTIVO')

        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(e['id_trabajador']))),
                    ft.DataCell(ft.Text(f"{e['nombre']} {e['ap_paterno']}")),
                    ft.DataCell(ft.Text(e['puesto'])),
                    ft.DataCell(ft.Text(e['turno'])),

                    ft.DataCell(
                        ft.Text(
                            estado,
                            color="green" if estado == "ACTIVO" else "red"
                        )
                    ),

                    ft.DataCell(
                        ft.Row(
                            [
                                # EDITAR
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda ev, emp=e: ir_a_editar(emp)
                                ),

                                # DESHABILITAR
                                ft.IconButton(
                                    icon=ft.Icons.CANCEL,
                                    icon_color="red",
                                    visible=estado == "ACTIVO",
                                    on_click=lambda ev, emp=e: confirmar_baja(emp)
                                ),

                                # ACTIVAR
                                ft.IconButton(
                                    icon=ft.Icons.CHECK_CIRCLE,
                                    icon_color="green",
                                    visible=estado == "INACTIVO",
                                    on_click=lambda ev, emp=e: activar(emp)
                                ),
                            ]
                        )
                    ),
                ]
            )
        )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Puesto")),
            ft.DataColumn(ft.Text("Turno")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=filas
    )

    # ---------------- UI ----------------
    return ft.View(
        route="/gestion_personal",
        controls=[
            ft.Row(
                [
                    ft.Text("Gestión de Personal", size=28, weight="bold"),
                    ft.ElevatedButton("Nuevo", icon=ft.Icons.ADD, on_click=ir_a_alta)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            ft.Divider(),

            ft.Container(tabla, expand=True),

            ft.ElevatedButton("Volver", on_click=volver)
        ]
    )