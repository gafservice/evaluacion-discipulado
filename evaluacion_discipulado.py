import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.patches as mpatches
from collections import Counter
import pandas as pd

# Cargar datos desde archivo CSV
df = pd.read_csv("respuestas_vida.csv")

# Habilidades en orden
habilidades = [
    "Manejo de emociones y sentimientos",
    "Manejo de tensiones y estrés",
    "Empatía",
    "Comunicación asertiva",
    "Relaciones interpersonales",
    "Manejo de problemas y conflictos",
    "Autoconocimiento",
    "Toma de decisiones",
    "Pensamiento creativo",
    "Pensamiento crítico"
]

# Colores personalizados
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

# Combinar selecciones de Parte 3
selecciones = list(df["Habilidad más desarrollada"].dropna()) + list(df["Habilidad que desea fortalecer"].dropna())
conteo = Counter(selecciones)
total = len(df) * 2  # Porque cada persona selecciona 2

# Datos para graficar
frecuencias = [conteo.get(h, 0) / total * 100 for h in habilidades]
colores = [colores_dict[h] for h in habilidades]

# Posiciones y tamaños
x_pos = np.arange(len(habilidades)) * 3.0
y_pos = np.zeros(len(habilidades))
z_pos = np.zeros(len(habilidades))
dx = np.ones(len(habilidades)) * 2.2
dy = np.ones(len(habilidades)) * 0.2
dz = frecuencias

# Crear figura
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')

# Dibujar barras
ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colores, shade=True)

# Estética de ejes
ax.view_init(elev=15, azim=-50)
ax.set_title("Frecuencia de Selección por Habilidad (Parte 3)", fontsize=14, pad=15)
ax.set_zlabel("Porcentaje (%)", labelpad=10)
ax.set_yticks([])
ax.set_xticks([])
ax.set_zlim(0, 100)

# Limpiar el fondo
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.pane.fill = False
    axis._axinfo["grid"].update({"linewidth": 0.2})

# Leyenda lateral
leyenda = [mpatches.Patch(color=colores[i], label=habilidades[i]) for i in range(len(habilidades))]
plt.legend(handles=leyenda, loc='center left', bbox_to_anchor=(1.25, 0.5), fontsize=9, frameon=False)

# Fuente
plt.figtext(0.05, 0.01, "Fuente: Autoevaluación anónima (Parte 3)", ha="left", fontsize=8, style='italic')

# Mostrar y guardar
plt.tight_layout()
plt.savefig("grafico_3D_porcentaje.png", dpi=300)
plt.show()
