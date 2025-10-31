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
