from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_payroll_pdf(
    empleado,
    fecha_pago,
    salario_mensual,
    salario_hora,
    salario_bruto,
    convenio,
    extra15,
    extra2,
    feriado,
    feriado2,
    comisiones,
    sem,
    ivm,
    banco,
    renta,
    embargos,
    total_devengado,
    total_deducciones,
    salario_neto
):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    y = 750

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, f"Recibo de Nómina - {empleado['nombre']}")
    y -= 30

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Puesto: {empleado['puesto']}")
    y -= 20
    pdf.drawString(50, y, f"Fecha de pago: {fecha_pago}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DEVENGADOS")
    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Salario base: ₡{salario_bruto:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Convenio: ₡{convenio:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Horas extra 1.5: ₡{extra15:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Horas extra 2x: ₡{extra2:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Feriado: ₡{feriado:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Feriado 2x: ₡{feriado2:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Comisiones: ₡{comisiones:,.0f}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DEDUCCIONES")
    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"SEM (5.5%): ₡{sem:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"IVM (4.33%): ₡{ivm:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Banco Popular (1%): ₡{banco:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Renta: ₡{renta:,.0f}")
    y -= 15
    pdf.drawString(50, y, f"Embargos: ₡{embargos:,.0f}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Neto a pagar: ₡{salario_neto:,.0f}")

    pdf.save()

    buffer.seek(0)
    return buffer
