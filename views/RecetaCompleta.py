import flet as ft
import asyncio
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def receta_completa_view(page: ft.Page, volver):

    now = datetime.now()
    fecha_actual = now.strftime("%Y-%m-%d")
    hora_actual = now.strftime("%H:%M")

    id_medico = ft.TextField(label="ID Médico", width=200)
    nombre_medico = ft.TextField(label="Nombre Médico", expand=True)

    cedula_medico = ft.TextField(
        label="Cédula Profesional",
        read_only=True,
        expand=True
    )
    
    
    id_paciente = ft.TextField(label="ID Paciente", width=150)

    nombre_paciente = ft.TextField(label="Nombre", expand=True)
    apellido_paciente = ft.TextField(label="Apellido", expand=True)

    edad_paciente = ft.TextField(label="Edad", width=100)

    diagnostico = ft.TextField(label="Diagnóstico", multiline=True, expand=True)
    firma = ft.TextField(label="Firma", expand=True)

    # LISTA PRESCRIPCION
    lista_medicamentos = ft.Column()

    def crear_fila():
        nombre = ft.TextField(label="Medicamento", expand=True)
        dosis = ft.TextField(label="Dosis", width=150)
        frecuencia = ft.TextField(label="Frecuencia", width=150)
        duracion = ft.TextField(label="Duración", width=150)

        fila = ft.Row()

        def eliminar_fila(e):
            lista_medicamentos.controls.remove(fila)
            page.update()

        btn_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color="red",
            on_click=eliminar_fila
        )

        fila.controls = [nombre, dosis, frecuencia, duracion, btn_eliminar]

        lista_medicamentos.controls.append(fila)
        page.update()

    # GENERACION PDF
    def generar_pdf(e):
        doc = SimpleDocTemplate("receta.pdf")
        styles = getSampleStyleSheet()
        elementos = []

        elementos.append(Paragraph("Receta Médica", styles["Title"]))
        elementos.append(Spacer(1, 10))

        elementos.append(Paragraph(f"Médico: {nombre_medico.value}", styles["Normal"]))
        elementos.append(Paragraph(f"Paciente ID: {id_paciente.value}", styles["Normal"]))
        elementos.append(Spacer(1, 10))

        elementos.append(Paragraph("Prescripción:", styles["Heading2"]))

        for fila in lista_medicamentos.controls:
            med = fila.controls[0].value
            dosis = fila.controls[1].value
            frecuencia = fila.controls[2].value
            duracion = fila.controls[3].value

            texto = f"Nombre del medicamento{med} - Dosis{dosis} - Frecuencia{frecuencia} - Duración{duracion}"
            elementos.append(Paragraph(texto, styles["Normal"]))

        doc.build(elementos)

        mensaje.value = "PDF generado correctamente"
        mensaje.color = "green"
        page.update()

    # ================== MENSAJE ==================
    mensaje = ft.Text()

    async def limpiar():
        await asyncio.sleep(3)
        mensaje.value = ""
        page.update()

    def guardar(e):
        mensaje.value = "Receta guardada"
        mensaje.color = "green"
        page.update()
        page.run_task(limpiar)

    # ================== UI ==================
    return ft.View(
        route="/receta_completa",
        controls=[
            ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Card(
                                    content=ft.Container(
                                        width=900,
                                        padding=25,
                                        content=ft.Column(
                                            [
                                                ft.Text("Receta Médica", size=26, weight="bold"),

                                                ft.Row([id_medico, nombre_medico]),
                                                ft.Row([cedula_medico]),
                                                ft.Row([id_paciente,nombre_paciente,apellido_paciente,edad_paciente]),

                                                diagnostico,

                                                ft.Divider(),

                                                ft.Text("Prescripción", weight="bold"),
                                                ft.Row([
                                                    ft.Text("Medicamento", expand=True),
                                                    ft.Text("dosis", width=150),
                                                    ft.Text("Frecuencia", width=150),
                                                    ft.Text("duracion", width=150),
                                                ]),

                                                lista_medicamentos,

                                                ft.ElevatedButton(
                                                    "Agregar medicamento",
                                                    icon=ft.Icons.ADD,
                                                    on_click=lambda e: crear_fila()
                                                ),

                                                firma,

                                                ft.Row(
                                                    [
                                                        ft.ElevatedButton("Guardar", on_click=guardar),
                                                        ft.ElevatedButton("Generar PDF", on_click=generar_pdf),
                                                        ft.ElevatedButton("Volver", on_click=volver),
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