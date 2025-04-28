# Evaluación de Discipulado - Dashboard Estético
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# Configurar página para 1920x1080
st.set_page_config(layout="wide")

# Inicializar sesión
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=[
        "Integridad", "Lealtad", "Fidelidad", "Firmeza", "Motivación", "Tacto", "Empatía"
    ])

st.title("Evaluación Anónima de Formación de Discípulos - Dashboard Avanzado")

st.subheader("Autoevaluación (Anónima)")

# Opciones resumidas
options = ["Domino", "Gen. Domino", "A Veces", "No Domino"]

# Formulario
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

    submitted = st.form_submit_button("Enviar respuesta")

# Guardar datos
if submitted:
    new_entry = {
        "Integridad": integridad,
        "Lealtad": lealtad,
        "Fidelidad": fidelidad,
        "Firmeza": firmeza,
        "Motivación": motivacion,
        "Tacto": tacto,
        "Empatía": empatia
    }
    st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([new_entry])], ignore_index=True)
    st.success("¡Respuesta registrada exitosamente!")

# Mostrar gráficos en dashboard
st.subheader("Resultados en tiempo real - Dashboard Estético")

if not st.session_state['data'].empty:
    areas = list(st.session_state['data'].columns)
    color_map = cm.get_cmap('viridis')

    # Primera fila
    cols = st.columns(4)
    for idx, area in enumerate(areas[:4]):
        with cols[idx]:
            conteo = st.session_state['data'][area].value_counts().reindex(options, fill_value=0)
            fig, ax = plt.subplots(figsize=(4, 3))
            bars = ax.bar(conteo.index, conteo.values, color=color_map(np.linspace(0.2, 0.8, 4)), edgecolor='black')
            ax.set_title(area, fontsize=12, weight='bold')
            ax.set_ylabel('Cantidad', fontsize=10)
            ax.set_ylim(0, max(conteo.values.max() + 1, 5))
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.set_facecolor('#f9f9f9')
            fig.patch.set_facecolor('#f0f2f6')
            st.pyplot(fig)

    # Segunda fila
    cols = st.columns(3)
    for idx, area in enumerate(areas[4:]):
        with cols[idx]:
            conteo = st.session_state['data'][area].value_counts().reindex(options, fill_value=0)
            fig, ax = plt.subplots(figsize=(4, 3))
            bars = ax.bar(conteo.index, conteo.values, color=color_map(np.linspace(0.2, 0.8, 4)), edgecolor='black')
            ax.set_title(area, fontsize=12, weight='bold')
            ax.set_ylabel('Cantidad', fontsize=10)
            ax.set_ylim(0, max(conteo.values.max() + 1, 5))
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.set_facecolor('#f9f9f9')
            fig.patch.set_facecolor('#f0f2f6')
            st.pyplot(fig)
else:
    st.info("Aún no hay respuestas registradas.")

