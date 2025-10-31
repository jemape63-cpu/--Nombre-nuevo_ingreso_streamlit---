import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import pandas as pd
import io

st.set_page_config(page_title="Nuevo Ingreso Clínico", layout="wide")
st.title("🩺 Extracción de datos clínicos desde PDF")

uploaded_file = st.file_uploader("📄 Selecciona un informe PDF", type="pdf")

if uploaded_file:
    st.success("✅ PDF cargado correctamente.")
    pages = convert_from_bytes(uploaded_file.read())
    texto = ""
    for page in pages:
        texto += pytesseract.image_to_string(page, lang='spa') + "\n"

    st.subheader("🧠 Texto extraído")
    st.text_area("Contenido OCR", texto, height=300)

    df = pd.DataFrame({"Texto extraído": [texto]})
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        writer.save()
        data = output.getvalue()

    st.download_button(
        label="💾 Descargar Excel",
        data=data,
        file_name="informe_clinico.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
