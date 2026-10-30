"""Generación de PDF para la factura asociada a un pedido."""
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from app.services.PedidoService import pedido_a_dict

def generar_factura_pdf(pedido) -> bytes:
    datos = pedido_a_dict(pedido)
    factura = datos.get("factura")
    if not factura:
        raise ValueError("El pedido no tiene una factura asociada.")

    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=0.65 * inch, leftMargin=0.65 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        title=f"Factura {factura['numero_factura']}",
        author="Café Lenca",
    )
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="CafeTitle", parent=estilos["Title"], alignment=TA_CENTER, fontSize=20, leading=24))
    estilos.add(ParagraphStyle(name="Right", parent=estilos["Normal"], alignment=TA_RIGHT))
    elementos = [
        Paragraph("Café Lenca", estilos["CafeTitle"]),
        Paragraph("Factura de venta", estilos["Heading2"]),
        Spacer(1, 8),
        Paragraph(f"<b>Número:</b> {factura['numero_factura']}", estilos["Normal"]),
        Paragraph(f"<b>Fecha:</b> {factura['fecha_emision']}", estilos["Normal"]),
        Paragraph(f"<b>Pedido:</b> {datos['idPedido']}", estilos["Normal"]),
        Spacer(1, 16),
    ]
    filas = [["Producto", "Cantidad", "Precio unitario", "Importe"]]
    for detalle in datos["detalles"]:
        filas.append([
            str(detalle["nombre_producto"] or f"Producto {detalle['Producto_idProducto']}"),
            str(detalle["cantidad"]),
            f"L {float(detalle['precio_unitario']):,.2f}",
            f"L {float(detalle['importe']):,.2f}",
        ])
    tabla = Table(filas, colWidths=[3.2 * inch, 0.8 * inch, 1.25 * inch, 1.25 * inch], repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#285943")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7F5")]),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    elementos.extend([tabla, Spacer(1, 16)])
    resumen = [
        ["Subtotal", f"L {float(factura['subtotal']):,.2f}"],
        ["Descuento", f"L {float(factura['descuento']):,.2f}"],
        ["Impuesto", f"L {float(factura['impuesto']):,.2f}"],
        ["TOTAL", f"L {float(factura['total']):,.2f}"],
    ]
    totales = Table(resumen, colWidths=[5.1 * inch, 1.4 * inch], hAlign="RIGHT")
    totales.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#285943")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elementos.extend([totales, Spacer(1, 24), Paragraph("¡Gracias por su visita!", estilos["Normal"])])
    documento.build(elementos)
    return buffer.getvalue()
