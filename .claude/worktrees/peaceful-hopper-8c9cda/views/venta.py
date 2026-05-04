import flet as ft
import asyncio
from database.consultas import buscar_medicamentos_bd, procesar_venta_completa

def caja_view(page: ft.Page, volver):

    # 1. VARIABLES DE ESTADO
    carrito = []

    # --- 2. CONTROLES VISUALES ---
    mensaje = ft.Text()
    txt_total = ft.Text("Total: $0.00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    lista_resultados = ft.ListView(expand=True, spacing=5)
    
    # Tabla con márgenes reducidos para que quepa el botón
    tabla_ticket = ft.DataTable(
        column_spacing=15,
        horizontal_margin=10,
        columns=[
            ft.DataColumn(ft.Text("Concepto")),
            ft.DataColumn(ft.Text("Cant."), numeric=True),
            ft.DataColumn(ft.Text("Importe"), numeric=True),
            ft.DataColumn(ft.Text("")), # Columna para el botón de eliminar
        ],
        rows=[]
    )

    buscador = ft.TextField(
        label="Buscar medicamento por nombre o código...", 
        prefix_icon=ft.Icons.SEARCH,
        expand=True
    )

    switch_consulta = ft.Switch(label="Consulta General ($500)", value=False)
    switch_emergencia = ft.Switch(label="Consulta de Emergencia ($800)", value=False)

    # --- 3. FUNCIONES LÓGICAS ---
    async def limpiar_mensaje():
        await asyncio.sleep(3)
        mensaje.value = ""
        page.update()

    def realizar_cobro(e):
        costo_servicios = 0.0
        tipo_consulta = "Ninguna"

        if switch_emergencia.value:
            costo_servicios = 800.0
            tipo_consulta = "Consulta de Emergencia"
        elif switch_consulta.value:
            costo_servicios = 500.0
            tipo_consulta = "Consulta General"
        
        # Sumamos el total de los productos en el carrito de forma segura
        total_medicamentos = sum(item["subtotal"] for item in carrito)
        total_final = total_medicamentos + costo_servicios

        if total_final == 0:
            mensaje.value = "Agrega productos o selecciona una consulta para cobrar."
            mensaje.color = "red"
            page.update()
            page.run_task(limpiar_mensaje)
            return
        
        ok, msj_res = procesar_venta_completa(total_final, tipo_consulta, carrito)

        if ok:
            mensaje.value = "¡Cobro realizado con éxito! Inventario actualizado."
            mensaje.color = "green"
            carrito.clear()
            switch_consulta.value = False
            switch_emergencia.value = False
            actualizar_ticket() # Limpiamos la tabla visual
        else:
            mensaje.value = msj_res
            mensaje.color = "red"

        page.update()
        page.run_task(limpiar_mensaje)

    def actualizar_ticket(e=None):
        tabla_ticket.rows.clear()
        total_productos = 0.0

        # Sub-función que "congela" los datos de cada artículo para que el botón de eliminar no se confunda
        def crear_fila(articulo):
            return ft.DataRow(cells=[
                ft.DataCell(ft.Text(articulo["nombre"])),
                ft.DataCell(ft.Text(str(articulo["cantidad"]))),
                ft.DataCell(ft.Text(f"${articulo['subtotal']:.2f}")),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="red",
                        on_click=lambda e: eliminar_del_carrito(articulo["id_medicamento"])
                    )
                )
            ])

        for item in carrito:
            tabla_ticket.rows.append(crear_fila(item))
            total_productos += item["subtotal"]

        costo_servicios = 0.0

        # Lógica para evitar que se cobren las dos consultas al mismo tiempo
        if e and e.control == switch_emergencia and switch_emergencia.value:
            switch_consulta.value = False
        elif e and e.control == switch_consulta and switch_consulta.value:
            switch_emergencia.value = False
        
        if switch_emergencia.value:
            costo_servicios = 800.0
        elif switch_consulta.value:
            costo_servicios = 500.0
        
        total_final = total_productos + costo_servicios
        txt_total.value = f"Total: ${total_final:.2f}"
        
        tabla_ticket.update()
        page.update()

    def agregar_al_carrito(medicamento):
        id_med = medicamento[0]
        nombre_med = medicamento[1]
        precio_med = float(medicamento[2])

        encontrado = False
        for item in carrito:
            if item["id_medicamento"] == id_med:
                item["cantidad"] += 1
                item["subtotal"] = item["cantidad"] * item["precio"]
                encontrado = True
                break
        
        if not encontrado:
            carrito.append({
                "id_medicamento": id_med,
                "nombre": nombre_med,
                "precio": precio_med,
                "cantidad": 1,
                "subtotal": precio_med
            })

        buscador.value = ""
        lista_resultados.controls.clear()
        actualizar_ticket()

    def eliminar_del_carrito(id_medicamento):
        for item in carrito:
            if item["id_medicamento"] == id_medicamento:
                carrito.remove(item)
                break
        actualizar_ticket()

    def realizar_busqueda(e):
        termino = buscador.value.strip()
        lista_resultados.controls.clear()

        if len(termino) > 0:
            resultados = buscar_medicamentos_bd(termino)

            for med in resultados:
                item_lista = ft.ListTile(
                    title=ft.Text(f"{med[1]} - ${med[2]:.2f} (Stock: {med[3]})"),
                    leading=ft.Icon(ft.Icons.MEDICAL_SERVICES, color=ft.Colors.GREEN),
                    on_click=lambda e, m=med: agregar_al_carrito(m)
                )
                lista_resultados.controls.append(item_lista)
        page.update()
    
    # --- 4. CONEXIÓN DE EVENTOS ---
    buscador.on_change = realizar_busqueda
    switch_consulta.on_change = actualizar_ticket
    switch_emergencia.on_change = actualizar_ticket

    # --- 5. ARMADO FINAL DE LA INTERFAZ ---
    btn_cobrar = ft.ElevatedButton(
        "Realizar Cobro", 
        icon=ft.Icons.PAYMENTS,
        on_click=realizar_cobro,
        style=ft.ButtonStyle(padding=20),
        expand=True
    )

    panel_izquierdo = ft.Column(
        expand=2,
        controls=[
            ft.Text("Agregar Conceptos", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([buscador, ft.IconButton(icon=ft.Icons.ADD_SHOPPING_CART)]),
            lista_resultados, 
            ft.Divider(),
            ft.Text("Servicios Médicos", size=16, weight=ft.FontWeight.W_600),
            switch_consulta,
            switch_emergencia,
            ft.Container(expand=True)
        ]
    )

    panel_derecho = ft.Card(
        expand=1,
        elevation=5,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Resumen de Venta", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    # Doble Scroll: Vertical para la lista, Horizontal para la tabla ancha
                    ft.Column(
                        controls=[
                            ft.Row([tabla_ticket], scroll=ft.ScrollMode.AUTO)
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                    ft.Divider(),
                    ft.Row([txt_total], alignment=ft.MainAxisAlignment.END),
                    ft.Row([btn_cobrar]),
                    mensaje
                ]
            )
        )
    )

    return ft.View(
        route="/caja",
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row([
                            ft.Text("Módulo de Caja", size=26, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton("Volver al Inicio", icon=ft.Icons.ARROW_BACK, on_click=volver)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Row(
                            expand=True,
                            controls=[panel_izquierdo, ft.VerticalDivider(), panel_derecho]
                        )
                    ]
                )
            )
        ]
    )