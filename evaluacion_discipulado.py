import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os

# Configuración de página
st.set_page_config(layout="wide")

# Inicializar el archivo de datos si no existe
if not os.path.exists("respuestas.csv"):
    df_init = pd.DataFrame(columns=[
        "Integridad", "Lealtad", "Fidelidad", "Firmeza", "Motivación", "Tacto", "Empatía"
    ])
    df_init.to_csv("respuestas.csv", index=False)

# Cargar datos existentes
data = pd.read_csv("respuestas.csv")

# Opciones resumidas
options = ["Siempre", "Casi Sí", "Casi No", "Nunca"]

st.title("Evaluación de Formación de Discípulos (Formulario Público)")

# --- Modo de Acceso ---
modo = st.sidebar.selectbox("Modo de uso:", ["Responder Formulario", "Modo Administrador"])

# --- Modo Público (solo formulario) ---
if modo == "Responder Formulario":
    st.subheader("Autoevaluación Anónima")

    with st.form("formulario"):
        col1, col2 = st.columns(2)
        with col1:
            integridad = st.radio("Integridad", options, key="integridad")
            lealtad = st.radio("Lealtad", options, key="lealtad")
            fidelidad = st.radio("Fidelidad", options, key="fidelidad")
        with col2:
            firmeza = st.radio("Firmeza", options, key="firmeza")
            motivacion = st.radio("Motivación", options, key="motivacion")
            tacto = st.radio("Tacto", options, key="tacto")
            empatia = st.radio("Empatía", options, key="empatia")

        enviado = st.form_submit_button("Enviar Respuesta")

    if enviado:
        nueva_respuesta = {
            "Integridad": integridad,
            "Lealtad": lealtad,
            "Fidelidad": fidelidad,
            "Firmeza": firmeza,
            "Motivación": motivacion,
            "Tacto": tacto,
            "Empatía": empatia
        }
        data = pd.concat([data, pd.DataFrame([nueva_respuesta])], ignore_index=True)
        data.to_csv("respuestas.csv", index=False)
        st.success("¡Gracias por tu participación! Tus respuestas han sido registradas.")

# --- Modo Admin (privado) ---
elif modo == "Modo Administrador":
    st.subheader("Panel de Administración")
    password = st.text_input("Ingrese la clave de administrador:", type="password")

    # Cambia esta clave por una segura para tu uso
    if password == "clave123":
        st.success("Acceso concedido. Mostrando resultados en vivo.")

        if not data.empty:
            areas = list(data.columns)
            color_map = cm.get_cmap('viridis')

            st.subheader("Resultados en tiempo real - Dashboard Privado")

            # Primera fila de gráficos
            cols = st.columns(4)
            for idx, area in enumerate(areas[:4]):
                with cols[idx]:
                    conteo = data[area].value_counts().reindex(options, fill_value=0)
                    fig, ax = plt.subplots(figsize=(4, 3))
                    bars = ax.bar(conteo.index, conteo.values, color=color_map(np.linspace(0.2, 0.8, 4)), edgecolor='black')
                    ax.set_title(area, fontsize=12, weight='bold')
                    ax.set_ylabel('Cantidad', fontsize=10)
                    ax.set_ylim(0, max(conteo.values.max() + 1, 5))
                    ax.grid(axis='y', linestyle='--', alpha=0.7)
                    ax.set_facecolor('#f9f9f9')
                    fig.patch.set_facecolor('#f0f2f6')
                    st.pyplot(fig)

            # Segunda fila de gráficos
            cols = st.columns(3)
            for idx, area in enumerate(areas[4:]):
                with cols[idx]:
                    conteo = data[area].value_counts().reindex(options, fill_value=0)
                    fig, ax = plt.subplots(figsize=(4, 3))
                    bars = ax.bar(conteo.index, conteo.values, color=color_map(np.linspace(0.2, 0.8, 4)), edgecolor='black')
                    ax.set_title(area, fontsize=12, weight='bold')
                    ax.set_ylabel('Cantidad', fontsize=10)
                    ax.set_ylim(0, max(conteo.values.max() + 1, 5))
                    ax.grid(axis='y', linestyle='--', alpha=0.7)
                    ax.set_facecolor('#f9f9f9')
                    fig.patch.set_facecolor('#f0f2f6')
                    st.pyplot(fig)

            st.download_button(
                label="Descargar datos en CSV",
                data=data.to_csv(index=False).encode('utf-8'),
                file_name='respuestas_discipulado.csv',
                mime='text/csv'
            )
        else:
            st.info("No hay datos registrados todavía.")
    else:
        if password != "":
            st.error("Clave incorrecta. Acceso denegado.")

