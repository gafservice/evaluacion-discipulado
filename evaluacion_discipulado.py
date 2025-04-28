import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os
from datetime import datetime

# Configuración de página
st.set_page_config(layout="wide")

# Inicializar archivo de datos
if not os.path.exists("respuestas.csv"):
    df_init = pd.DataFrame(columns=[
        "Integridad", "Lealtad", "Fidelidad", "Firmeza", "Motivación", "Tacto", "Empatía"
    ])
    df_init.to_csv("respuestas.csv", index=False)

# Cargar datos existentes
data = pd.read_csv("respuestas.csv")

# Opciones de respuesta
options = ["Siempre", "Casi Sí", "Casi No", "Nunca"]
puntaje_opciones = {"Siempre": 4, "Casi Sí": 3, "Casi No": 2, "Nunca": 1}

st.title("Características que te equipan como discípulo")

# --- Modo de Acceso ---
modo = st.sidebar.selectbox("Modo de uso:", ["Responder Formulario", "Modo Administrador"])

# --- Modo Público ---
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

# --- Modo Administrador ---
elif modo == "Modo Administrador":
    st.subheader("Panel de Administración")
    password = st.text_input("Ingrese la clave de administrador:", type="password")

    if password == "clave123":
        st.success("Acceso concedido. Mostrando resultados en vivo.")

        if not data.empty:
            areas = list(data.columns)
            color_map = cm.get_cmap('viridis')

            st.subheader("Resultados en tiempo real - Dashboard Privado")

            # Gráficos
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
                label="Descargar datos actuales en CSV",
                data=data.to_csv(index=False).encode('utf-8'),
                file_name='respuestas_discipulado.csv',
                mime='text/csv'
            )

            st.markdown("---")

            # Análisis de resultados
            st.subheader("🔎 Análisis y Sugerencias de Mejora")

            promedio_areas = {}
            for area in areas:
                valores = data[area].map(puntaje_opciones)
                promedio = valores.mean()
                promedio_areas[area] = promedio

            for area, promedio in promedio_areas.items():
                if promedio >= 3.5:
                    st.success(f"✅ {area}: Excelente nivel (Promedio: {promedio:.2f})")
                elif 3.0 <= promedio < 3.5:
                    st.info(f"ℹ️ {area}: Buen nivel (Promedio: {promedio:.2f})")
                elif 2.0 <= promedio < 3.0:
                    st.warning(f"⚠️ {area}: Nivel Regular (Promedio: {promedio:.2f}) ➔ Reforzar con prácticas diarias y mentoría espiritual.")
                else:
                    st.error(f"❗ {area}: Nivel Bajo (Promedio: {promedio:.2f}) ➔ Urgente fortalecer mediante devocionales, acompañamiento y discipulado cercano.")

            st.markdown("---")
            if st.button("Guardar respaldo y reiniciar evaluación"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"respuestas_backup_{timestamp}.csv"
                data.to_csv(backup_filename, index=False)
                st.success(f"Respaldo guardado como {backup_filename}.")

                df_empty = pd.DataFrame(columns=data.columns)
                df_empty.to_csv("respuestas.csv", index=False)
                st.success("¡Evaluación reiniciada exitosamente! Recargá la página para ver el formulario vacío.")

        else:
            st.info("No hay datos registrados todavía.")
    else:
        if password != "":
            st.error("Clave incorrecta. Acceso denegado.")

