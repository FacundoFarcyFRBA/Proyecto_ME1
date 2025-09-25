#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 12:08:03 2025

@author: facu
"""

import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
#%% Con platypus

# --- Datos para la tabla ---
data = {
    'Producto': ['A', 'B', 'C'],
    'Ventas': [150, 200, 300]
}
df = pd.DataFrame(data)

# --- Crear gráfico ---
plt.bar(df['Producto'], df['Ventas'], color='skyblue')
plt.title('Ventas por Producto')
plt.xlabel('Producto')
plt.ylabel('Ventas')
plt.savefig('grafico.png')
plt.close()

# --- Crear PDF ---
pdf = SimpleDocTemplate("reporte.pdf", pagesize=letter)
elementos = []

# --- Convertir DataFrame en tabla para ReportLab ---
tabla = Table([df.columns.tolist()] + df.values.tolist())
tabla.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
]))

elementos.append(tabla)

# --- Agregar gráfico ---
elementos.append(Image('grafico.png', width=400, height=300))

# --- Generar PDF ---
pdf.build(elementos)
print("PDF generado con éxito.")

#%% con canvas (posición absoluta, menos propiedades)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("reporte_posiciones.pdf", pagesize=A4)
width, height = A4  # dimensiones de la página

# Dibujar texto
c.drawString(100, height-100, "Hola, mundo")  # x=100, y=altura-100

# Dibujar gráfico como imagen en posición exacta
c.drawImage("grafico.png", x=50, y=height-400, width=400, height=300)

# Dibujar tabla manualmente
data = [["Producto", "Cantidad", "Precio"], ["Manzanas", 10, 50]]
x0, y0 = 50, height-500  # posición superior izquierda de la tabla
row_height = 20
col_widths = [100, 100, 100]

for i, row in enumerate(data):
    for j, cell in enumerate(row):
        c.drawString(x0 + j*col_widths[j], y0 - i*row_height, str(cell))

c.showPage()
c.save()
#%% sin canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image

# Crear documento PDF
pdf = SimpleDocTemplate("reporte.pdf", pagesize=A4)
elements = []

# Tabla de ejemplo
data = [
    ["Producto", "Cantidad", "Precio"],
    ["Manzanas", 10, 50],
    ["Naranjas", 5, 30],
    ["Bananas", 7, 20]
]

table = Table(data)
# Estilo de tabla
style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.gray),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
])
table.setStyle(style)

elements.append(table)

# Agregar el gráfico
img = Image("grafico.png", width=400, height=300)
elements.append(img)

# Generar PDF
pdf.build(elements)

#%% TABLAS SIN USAR PANDAS
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# Crear PDF
pdf = SimpleDocTemplate("tabla_sin_pandas-b.pdf", pagesize=A4)
elements = []

# Datos de la tabla (lista de listas)
data = [
    ["Producto", "Cantidad", "Precio"],  # fila de encabezado
    ["Manzanas", 10, 50],
    ["Naranjas", 5, 30],
    ["Bananas", 7, 20]
]

# Crear tabla
table = Table(data, colWidths=[150, 100, 100], rowHeights=25)

# Estilo de tabla
style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.gray),       # fondo del encabezado
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),  # color del texto del encabezado
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),             # alinear todo al centro
    ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),            # alinear verticalmente
    ('GRID', (0,0), (-1,-1), 1, colors.black)        # dibujar las líneas de la cuadrícula
])
table.setStyle(style)

# Agregar la tabla al PDF
elements.append(table)

# Generar PDF
pdf.build(elements)

#%% JUNTAR TABLAS
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

pdf = SimpleDocTemplate("dos_tablas_misma_altura.pdf", pagesize=A4)
elements = []

# Tabla izquierda
data_left = [
    ["Producto", "Cantidad"],
    ["Manzanas", 10],
    ["Naranjas", 5]
]
table_left = Table(data_left, colWidths=[150, 100], rowHeights=25)
table_left.setStyle(TableStyle([
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)
]))

# Tabla derecha
data_right = [
    ["Producto", "Precio"],
    ["Manzanas", 50],
    ["Naranjas", 30]
]
table_right = Table(data_right, colWidths=[100, 100], rowHeights=25)
table_right.setStyle(TableStyle([
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)
]))

# Contenedor: tabla de 1 fila x 2 columnas
container = Table([[table_left, table_right]], colWidths=[250, 250])
container.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),   # misma altura vertical
    ('ALIGN', (0,0), (0,0), 'LEFT'),     # tabla izquierda
    ('ALIGN', (1,0), (1,0), 'RIGHT')     # tabla derecha
]))

elements.append(container)
pdf.build(elements)
#%%
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4

def encabezado(canvas, doc):
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(50, 820, "Mi Encabezado - Informe de Ejemplo")

pdf = SimpleDocTemplate("con_encabezado.pdf", pagesize=A4)
elements = []

# Ejemplo simple de tabla
data = [["Producto","Cantidad"], ["Manzanas",10], ["Naranjas",5]]
table = Table(data)
elements.append(table)

# Generar PDF con encabezado
pdf.build(elements, onFirstPage=encabezado, onLaterPages=encabezado)

# %% Unir celdas

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

doc = SimpleDocTemplate("ejemplo_span_color.pdf", pagesize=A4)

# Definimos 4 columnas (ancho total adaptado)
data = [
    # Queremos que esta fila *parezca* de 3 columnas:
    ["Enc A", "Enc B", "Enc C", ""],   # la última celda la vamos a spannear con la anterior
    # Siguiente fila con 4 columnas reales:
    ["r1c1", "r1c2", "r1c3", "r1c4"],
    ["r2c1", "r2c2", "r2c3", "r2c4"],
    ["r3c1", "r3c2", "r3c3", "r3c4"],
]

table = Table(data, colWidths=[120,120,120,120], rowHeights=25)

style = TableStyle([
    # 1) Hacemos que la primera fila tenga solo 3 "visibles":
    ('SPAN', (2,0), (3,0)),   # une la celda (fila0,col2) con (fila0,col3)
    # 2) Colorear filas específicas
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),  # color fila 0 (encabezado "3 cols")
    ('BACKGROUND', (0,1), (-1,1), colors.whitesmoke), # fila siguiente color distinto
    ('BACKGROUND', (0,3), (-1,3), colors.lightyellow),# otra fila cualquiera (fila 3)
    # 3) Bordes y alineación y fuente
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
])

table.setStyle(style)

doc.build([table])
# %% EJEMPLO PINTAR O NO BORDES
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

doc = SimpleDocTemplate("tabla_lineas_selectivas.pdf", pagesize=A4)

data = [
    ["Col1", "Col2", "Col3"],
    ["A", "B", "C"],
    ["1", "2", "3"],
    ["X", "Y", "Z"],
]

tabla = Table(data, colWidths=[100, 100, 100])

style = TableStyle([
    # Encabezado con fondo gris y bordes visibles
    ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
    ("GRID", (0,0), (-1,0), 1, colors.black),

    # Fila 1 sin bordes
    ("GRID", (0,1), (-1,1), 0, None),

    # Fila 2 con bordes
    ("GRID", (0,2), (-1,2), 0.5, colors.black),

    # Fila 3 sin bordes
    ("GRID", (0,3), (-1,3), 0, None),

    # Fuente general
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
])

tabla.setStyle(style)

doc.build([tabla])


# %%

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from reportlab.lib.pagesizes import A4
# Crear documento PDF
doc = SimpleDocTemplate("tabla_simple.pdf", pagesize=A4)

# Datos de ejemplo 3x3 (texto simple)
data_n = [
    ["Encabezado 1", "Encabezado 2", "Encabezado 3"],
    ["Fila1-Col1", "Fila1-Col2", "Fila1-Col3"],
    ["Fila2-Col1", "Fila2-Col2", "Fila2-Col3"]
]

# Crear tabla
tabla = Table(data_n)

# Estilo de la tabla: fondo y borde
tabla.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.lightblue),  # fila 0 con fondo azul
    # ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke), # resto de filas con gris claro
    # ("BOX", (0,0), (-1,-1), 2, colors.black),         # borde externo
    # ("VALIGN", (0,0), (-1,-1), "MIDDLE"),             # alineación vertical
    # ("ALIGN", (0,0), (-1,-1), "CENTER")              # alineación horizontal
]))

# Construir PDF
doc.build([tabla])
