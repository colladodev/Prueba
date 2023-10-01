import streamlit as st
import pandas as pd
import base64

# Variable global para almacenar el DataFrame original
original_df = None
# Variable global para almacenar el DataFrame del segundo archivo
second_df = None

def main():
    global original_df
    global second_df

    st.title("Actualización y Descarga de archivos CSV")
    st.sidebar.title("Configuración")

    # Agrega un componente de carga de archivos en la barra lateral para el archivo original
    uploaded_original_file = st.sidebar.file_uploader("Cargar el archivo CSV original", type=["csv"])

    # Agrega un componente de carga de archivos en la barra lateral para el segundo archivo
    uploaded_second_file = st.sidebar.file_uploader("Cargar el segundo archivo CSV", type=["csv"])

    # Si se ha cargado el archivo CSV original, muestra sus datos
    if uploaded_original_file is not None:
        st.sidebar.subheader("Configuración de visualización")
        encoding = st.sidebar.selectbox(
            "Seleccione la codificación del archivo CSV original", ["UTF-8", "ISO-8859-1"]
        )
        separator = st.sidebar.selectbox(
            "Seleccione el separador de columnas del archivo CSV original", [",", ";", "\t"]
        )

        try:
            original_df = pd.read_csv(uploaded_original_file, encoding=encoding, sep=separator)

            # Muestra el DataFrame original en Streamlit
            st.write("Vista previa del DataFrame original:")
            st.dataframe(original_df)
        except Exception as e:
            st.error(f"Error al cargar el archivo CSV original: {e}")

    # Si se ha cargado el segundo archivo CSV, muestra sus datos
    if uploaded_second_file is not None:
        st.sidebar.subheader("Configuración del segundo archivo")
        encoding = st.sidebar.selectbox(
            "Seleccione la codificación del segundo archivo CSV", ["UTF-8", "ISO-8859-1"]
        )
        separator = st.sidebar.selectbox(
            "Seleccione el separador de columnas del segundo archivo CSV", [",", ";", "\t"]
        )

        try:
            second_df = pd.read_csv(uploaded_second_file, encoding=encoding, sep=separator)

            # Muestra el DataFrame del segundo archivo en Streamlit
            st.write("Vista previa del segundo DataFrame:")
            st.dataframe(second_df)

            if st.button("Actualizar DataFrames"):
                # Realiza la fusión de DataFrames en función de las columnas que desees
                merged_df = original_df.merge(second_df[['INS_N', 'ENC_DATE', 'value']], left_on="Member Number", right_on="INS_N", how="left")

                # Actualiza las columnas 'DOS' y 'VALUE' del DataFrame original
                original_df['DOS'] = merged_df['ENC_DATE']
                original_df['VALUE'] = merged_df['value']

                # Muestra el DataFrame actualizado en Streamlit
                st.write("Vista previa del DataFrame actualizado:")
                st.dataframe(original_df)

                # Agregar botón de descarga
                st.markdown(get_download_link(original_df), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error al cargar el segundo archivo CSV: {e}")

def get_download_link(df):
    # Genera un enlace de descarga para el DataFrame actualizado en formato CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Descargar DataFrame Actualizado</a>'
    return href

if __name__ == "__main__":
    main()
