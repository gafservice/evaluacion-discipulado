import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import numpy as np
import os
from datetime import datetime
from collections import Counter

st.set_page_config(layout="wide")

# Habilidades base y extra
habilidades_base = [
    "Manejo de emociones y sentimientos", "Manejo de tensiones y estrés", "Empatía",
    "Comunicación asertiva", "Relaciones interpersonales", "Manejo de problemas y conflictos",
    "Autoconocimiento", "Toma de decisiones", "Pensamiento creativo", "Pensamiento crítico"
]
habilidades_extra = [
    "Habilidad más desarrollada", "Habilidad que desea fortalecer",
    "Reacción ante enojo de compañero", "Manejo del estrés", "Toma de decisiones difíciles"
]
habilidades = habilidades_base + habilidades_extra

# Opciones y codificación
options_base = ["1 - Nunca", "2 - Raramente", "3 - A veces", "4 - Frecuentemente", "5 - Siempre"]
puntaje_opciones = {opt: i + 1 for i, opt in enumerate(options_base)}
opciones_habilidad = habilidades_base

opciones_enojado = [
    "Me alejo o ignoro el problema", "Le devuelvo el enojo",
    "Intento hablar y aclarar con respeto", "Le pido ayuda a alguien para mediar"
]
opciones_estres = [
    "Me bloqueo o me enojo", "Busco distraerme con algo",
    "Intento organizarme o hablar con alguien", "Aplico alguna técnica que me ayude a relajarme"
]
opciones_decisiones = [
    "Elijo al azar o por impulso", "Pregunto a un amigo o familiar", "Analizo consecuencias antes de decidir"
]

# Archivo
archivo_csv = "respuestas_vida.csv"
if not os.path.exists(archivo_csv):
    pd.DataFrame(columns=habilidades).to_csv(archivo_csv, index=False)

@st.cache_data(ttl=5)
def cargar_datos():
    return pd.read_csv(archivo_csv)

# Interfaz
st.title("Autoevaluación Anónima: Habilidades para la Vida")
modo = st.sidebar.selectbox("Modo de uso", ["Responder Formulario", "Modo Administrador"])

if modo == "Responder Formulario":
    st.subheader("Parte 1: Autoevaluación (1 = Nunca, 5 = Siempre)")
    with st.form("formulario"):
        respuestas = {}
        for h in habilidades_base:
            respuestas[h] = st.radio(f"¿Con qué frecuencia sentís que... {h.lower()}?", options_base, index=None)

        st.subheader("Parte 2: Situaciones cotidianas")
        respuestas["Reacción ante enojo de compañero"] = st.radio("Si un compañero se enoja con vos...", opciones_enojado, index=None)
        respuestas["Manejo del estrés"] = st.radio("Cuando te sentís estresado o presionado:", opciones_estres, index=None)
        respuestas["Toma de decisiones difíciles"] = st.radio("Si tenés que decidir entre dos opciones difíciles:", opciones_decisiones, index=None)

        st.subheader("Parte 3: Seleccioná una opción")
        respuestas["Habilidad más desarrollada"] = st.selectbox("¿Cuál habilidad considerás que tenés más desarrollada?", opciones_habilidad, index=None)
        respuestas["Habilidad que desea fortalecer"] = st.selectbox("¿Cuál habilidad te gustaría fortalecer más?", opciones_habilidad, index=None)

        enviado = st.form_submit_button("Enviar Respuesta")

    if enviado:
        df = cargar_datos()
        df = pd.concat([df, pd.DataFrame([respuestas])], ignore_index=True)
        df.to_csv(archivo_csv, index=False)
        st.success("✅ ¡Gracias! Tus respuestas se han guardado.")

elif modo == "Modo Administrador":
    st.subheader("Panel de Administración")
    clave = st.text_input("Clave de administrador:", type="password")

    if clave == "clave123":
        opcion = st.selectbox("Sección", [
            "Análisis de Resultados",
            "Gráfico de Barras Comparativo",
            "Gráfico 3D de Selección",
            "Respaldar y Reiniciar"
        ])

        if st.button("🔄 Refrescar"):
            st.cache_data.clear()
            st.rerun()

        df = cargar_datos()

        if opcion == "Análisis de Resultados":
            st.subheader("📋 Análisis de Habilidades con Más Dificultad")
            if not df.empty:
                promedios = {h: df[h].map(puntaje_opciones).mean() for h in habilidades_base}
                ordenado = sorted(promedios.items(), key=lambda x: x[1])

                st.markdown("### 🛑 Habilidades más débiles")
                for h, p in ordenado[:3]:
                    st.error(f"❗ {h}: Bajo desarrollo percibido (Promedio: {p:.2f})")
            else:
                st.info("No hay datos para analizar.")

        elif opcion == "Gráfico de Barras Comparativo":
            st.subheader("📊 Comparación por Habilidad (Promedios)")
            if not df.empty:
                promedios = {h: df[h].map(puntaje_opciones).mean() for h in habilidades_base}
                ordenado = sorted(promedios.items(), key=lambda x: x[1])
                etiquetas = [x[0] for x in ordenado]
                valores = [x[1] for x in ordenado]
                colores = ["#d62728" if v < 3 else "#ff7f0e" if v < 4 else "#2ca02c" for v in valores]

                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(etiquetas, valores, color=colores, edgecolor='black')
                ax.set_xlim(1, 5)
                ax.set_xlabel("Promedio")
                ax.set_title("Nivel percibido por habilidad")
                ax.invert_yaxis()
                ax.grid(axis='x', linestyle='--', alpha=0.5)
                st.pyplot(fig)
            else:
                st.info("No hay datos registrados.")

        elif opcion == "Gráfico 3D de Selección":
            st.subheader("🧊 Visualización 3D de la Parte 3")
            if not df.empty:
                habilidades = habilidades_base
                colores_dict = {
                    "Manejo de emociones y sentimientos": "#666666",
                    "Manejo de tensiones y estrés": "#2E8B57",
                    "Empatía": "#4682B4",
                    "Comunicación asertiva": "#C71585",
                    "Relaciones interpersonales": "#FFD700",
                    "Manejo de problemas y conflictos": "#20B2AA",
                    "Autoconocimiento": "#8A2BE2",
                    "Toma de decisiones": "#FF8C00",
                    "Pensamiento creativo": "#6495ED",
                    "Pensamiento crítico": "#DC143C"
                }
                seleccion = list(df["Habilidad más desarrollada"].dropna()) + list(df["Habilidad que desea fortalecer"].dropna())
                conteo = Counter(seleccion)
                total = len(df) * 2
                porcentajes = [conteo.get(h, 0) / total * 100 for h in habilidades]
                colores = [colores_dict[h] for h in habilidades]

                x_pos = np.arange(len(habilidades)) * 3.0
                y_pos = np.zeros(len(habilidades))
                z_pos = np.zeros(len(habilidades))
                dx = np.ones(len(habilidades)) * 2.2
                dy = np.ones(len(habilidades)) * 0.2
                dz = porcentajes

                fig = plt.figure(figsize=(12, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colores, shade=True)
                ax.view_init(elev=15, azim=-50)
                ax.set_title("Frecuencia de Selección por Habilidad (Parte 3)", fontsize=14, pad=15)
                ax.set_zlabel("Porcentaje (%)", labelpad=10)
                ax.set_yticks([])
                ax.set_xticks([])
                ax.set_zlim(0, 100)
                for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
                    axis.pane.fill = False
                    axis._axinfo["grid"].update({"linewidth": 0.2})
                leyenda = [mpatches.Patch(color=colores[i], label=habilidades[i]) for i in range(len(habilidades))]
                plt.legend(handles=leyenda, loc='center left', bbox_to_anchor=(1.25, 0.5), fontsize=9, frameon=False)
                plt.figtext(0.05, 0.01, "Fuente: Autoevaluación anónima (Parte 3)", ha="left", fontsize=8, style='italic')
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("No hay datos disponibles para el gráfico 3D.")

        elif opcion == "Respaldar y Reiniciar":
            if not df.empty and st.button("📥 Guardar respaldo y reiniciar"):
                archivo = f"respaldo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(archivo, index=False)
                st.success(f"Datos respaldados como {archivo}")
                pd.DataFrame(columns=habilidades).to_csv(archivo_csv, index=False)
                st.success("Evaluación reiniciada correctamente.")
    else:
        if clave:
            st.error("Clave incorrecta.")
