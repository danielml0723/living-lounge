import streamlit as st
from modules.storage import load_employees
from modules.pdf_generator import generate_payroll_pdf

st.set_page_config(
    page_title="Sistema RRHH Nómina",
    layout="wide"
)

st.title("🏢 Sistema RRHH — Nómina")

st.markdown("""
### Living Lounge S.A.
**Cédula Jurídica:** 3-101-663107  
**Teléfono:** 2290-8788  
**Dirección:** Sabana Oeste, 400 mts oeste, frente a Cemaco
""")

c1, c2, c3 = st.columns(3)

with c1:
    fecha_desde = st.date_input("Fecha Desde")

with c2:
    fecha_hasta = st.date_input("Fecha Hasta")

with c3:
    tipo_planilla = st.selectbox("Tipo Planilla", ["Semanal", "Quincenal", "Mensual"])

st.divider()

df = load_employees()

st.metric("Colaboradores", len(df))
st.metric("Salario Base Total", f"₡{df['salario_mensual'].sum():,.0f}")

st.divider()

payroll_results = []

for idx, row in df.iterrows():

    salario_mensual = float(row["salario_mensual"])
    salario_diario = salario_mensual / 30
    salario_hora = salario_diario / 8

    with st.expander(f"{row['nombre']} | {row['puesto']}"):

        st.write(f"Salario hora: ₡{salario_hora:,.2f}")

        horas_bruto = st.number_input("Horas base", value=48.0, key=f"h_{idx}")
        extra15 = st.number_input("Horas extra 1.5", value=0.0, key=f"x15_{idx}")
        extra2 = st.number_input("Horas extra 2x", value=0.0, key=f"x2_{idx}")
        comisiones = st.number_input("Comisiones", value=0.0, key=f"com_{idx}")
        renta = st.number_input("Renta", value=0.0, key=f"r_{idx}")
        embargos = st.number_input("Embargos", value=0.0, key=f"e_{idx}")

        salario_bruto = horas_bruto * salario_hora
        convenio = 0
        feriado = 0
        feriado2 = 0

        total_devengado = salario_bruto + (extra15 * salario_hora * 1.5) + (extra2 * salario_hora * 2) + comisiones

        sem = total_devengado * 0.055
        ivm = total_devengado * 0.0433
        banco = total_devengado * 0.01

        total_deducciones = sem + ivm + banco + renta + embargos
        salario_neto = total_devengado - total_deducciones

        payroll_results.append({
            "empleado": row,
            "salario_mensual": salario_mensual,
            "salario_hora": salario_hora,
            "salario_bruto": salario_bruto,
            "convenio": convenio,
            "extra15": extra15,
            "extra2": extra2,
            "feriado": feriado,
            "feriado2": feriado2,
            "comisiones": comisiones,
            "sem": sem,
            "ivm": ivm,
            "banco": banco,
            "renta": renta,
            "embargos": embargos,
            "total_devengado": total_devengado,
            "total_deducciones": total_deducciones,
            "salario_neto": salario_neto
        })

st.divider()

# 🔥 DESCARGA DIRECTA SIN DISCO
st.subheader("📄 Descarga de PDFs")

fecha_pago = fecha_hasta.strftime("%Y-%m-%d")

for p in payroll_results:

    pdf_buffer = generate_payroll_pdf(
        empleado=p["empleado"],
        fecha_pago=fecha_pago,
        salario_mensual=p["salario_mensual"],
        salario_hora=p["salario_hora"],
        salario_bruto=p["salario_bruto"],
        convenio=p["convenio"],
        extra15=p["extra15"],
        extra2=p["extra2"],
        feriado=p["feriado"],
        feriado2=p["feriado2"],
        comisiones=p["comisiones"],
        sem=p["sem"],
        ivm=p["ivm"],
        banco=p["banco"],
        renta=p["renta"],
        embargos=p["embargos"],
        total_devengado=p["total_devengado"],
        total_deducciones=p["total_deducciones"],
        salario_neto=p["salario_neto"]
    )

    st.download_button(
        label=f"⬇️ Descargar {p['empleado']['nombre']}",
        data=pdf_buffer,
        file_name=f"nomina_{p['empleado']['nombre']}.pdf",
        mime="application/pdf"
    )
