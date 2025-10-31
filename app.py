import streamlit as st
import pdfplumber
import pandas as pd
import io

st.set_page_config(page_title="Extracción de texto clínico", layout="wide")
st.title("📄 Extracción de texto desde PDF")

uploaded_file = st.file_uploader("Selecciona un informe PDF", type="pdf")

if uploaded_file:
    st.success("✅ PDF cargado correctamente.")
    texto = ""

    # Extraer texto con pdfplumber
    with pdfplumber.open(uploaded_file) as pdf:
        for i, pagina in enumerate(pdf.pages):
            contenido = pagina.extract_text()
            texto += f"\n--- Página {i+1} ---\n{contenido}\n" if contenido else ""

    # Mostrar texto extraído
    st.subheader("🧠 Texto extraído")
    st.text_area("Contenido del PDF", texto, height=300)

    # Exportar a Excel
    df = pd.DataFrame({"Texto extraído": [texto]})
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    data = output.getvalue()

    st.download_button(
        label="💾 Descargar Excel",
        data=data,
        file_name="informe_clinico.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
