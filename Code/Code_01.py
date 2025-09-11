# ============================================================
# Taller 3: Doing Economics - Midiendo la temperatura de la Tierra y el CO₂
# Curso: Haciendo Economía
# Integrantes:
#   - Juan David Paiva
#   - Samuel Blanco Castellanos
#   - Sofía Obando
#
# Descripción:
# Este script en Python analiza anomalías de temperatura y concentraciones
# de CO₂ para estudiar patrones de cambio climático segun lo propuesto por el taller 3. 
# 
# Incluye:
#   - Lectura y procesamiento de datos climáticos (NASA, Mauna Loa)
#   - Cálculo de estadísticas descriptivas (medias, varianzas, cuantiles)
#   - Construcción de gráficos de líneas, histogramas y diagramas de dispersión
#   - Comparación de periodos históricos en temperatura y CO₂
#
# Nota: El código está organizado siguiendo la estructura de carpetas del curso
# (RawData, Scripts, Outputs), y se ejecuta en un entorno Anaconda.
# ============================================================
#Cargar Librerias 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pingouin as pg
plt.style.use(
    "https://raw.githubusercontent.com/aeturrell/core_python/main/plot_style.txt"
)
from scipy.stats import pearsonr

# Ruta principal del Taller que se debe ajustar segun donde esté guardado
base_path = Path(r"C:\Users\Lenovo\Documents\Universidad\Material Clases\Haciendo Economía\Taller3")

# Subcarpetas
rawdata_path = base_path / "Rawdata"
scripts_path = base_path / "Scripts"
outputs_path = base_path / "Outputs"
figures_path = outputs_path / "Figures"
figures_path.mkdir(parents=True, exist_ok=True) 
tables_path = base_path / "Outputs" / "Tables"
tables_path.mkdir(parents=True, exist_ok=True) 

#PRIMERA SECCIÓN 

# Archivo de anomalías de temperatura
# Leer el CSV
df = pd.read_csv(rawdata_path / "temp_deviation.csv")
print(df.head())
#Realizar la respectiva limpieza de la base RAW
df = pd.read_csv(
    rawdata_path / "temp_deviation.csv",
    skiprows=1,          # salta la primera fila de texto
    na_values="***"      # convierte *** en NaN automáticamente
)
print(df.head())
print(df.info())
# Asegurar que Year es numérico (por si quedó como string)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
# Poner Year como índice y ordenar
df = df.set_index("Year").sort_index()
print(df.index.name)   # debería mostrar 'Year'
print(df.head())

#GRAFICAS 1.1.2 Y 1.1.3
#Establecemos un diccionario de meses y colores correspondientes para las graficas
colores = {
    "Jan": "red", "Feb": "orange", "Mar": "gold",
    "Apr": "green", "May": "lime", "Jun": "cyan",
    "Jul": "blue", "Aug": "navy", "Sep": "purple",
    "Oct": "magenta", "Nov": "brown", "Dec": "black"
}

meses = {
    "Jan": "enero", "Feb": "febrero", "Mar": "marzo",
    "Apr": "abril", "May": "mayo", "Jun": "junio",
    "Jul": "julio", "Aug": "agosto", "Sep": "septiembre",
    "Oct": "octubre", "Nov": "noviembre", "Dec": "diciembre"
}

#Se selecciona el mes de preferencia
mes = "Mar"  
if mes not in df.columns:
    raise ValueError(f"La columna {mes} no existe en el DataFrame. Revisa df.columns")

# --- construir el gráfico  i)-------------------------
fig, ax = plt.subplots(figsize=(10, 5))
serie = df[mes].dropna()
ax.plot(serie.index, serie.values, color=colores[mes], linewidth=2, label=meses[mes].capitalize())
# línea horizontal en 0 (promedio 1951–1980)
ax.axhline(0, color="blue", linestyle="--", linewidth=1)
ax.text(serie.index.min(), 0.05, "promedio de 1951 a 1980", color="blue", fontsize=9)
# títulos y etiquetas
ax.set_title(f"Figura 1.1: Anomalía de temperatura en {meses[mes]} (1880 - {int(serie.index.max())})", fontsize=14)
ax.set_xlabel("Año")
ax.set_ylabel("Anomalía de temperatura (°C)")
ax.grid(True, alpha=0.3)
ax.legend()
# --- guardar figura 1---
filename = f"anomalia_{mes}.png"
fig.savefig(figures_path / filename, dpi=300, bbox_inches="tight")
plt.close(fig)  
#--------------------------------------------------------------------------------------------------------
#Construir Grafico ii)
# --- colores para estaciones ---
colores_estaciones = {
    "DJF": "red",     # diciembre-enero-febrero
    "MAM": "green",   # marzo-abril-mayo
    "JJA": "orange",  # junio-julio-agosto
    "SON": "purple"   # septiembre-octubre-noviembre
}
fig, ax = plt.subplots(figsize=(10, 6))
for estacion in ["DJF", "MAM", "JJA", "SON"]:
    serie = df[estacion].dropna()
    ax.plot(serie.index, serie.values, label=estacion,
            color=colores_estaciones[estacion], linewidth=2)
# Línea horizontal en 0
ax.axhline(0, color="blue", linestyle="--", linewidth=1)
ax.text(df.index.min(), 0.05, "promedio de 1951 a 1980", color="blue", fontsize=9)
# Títulos y etiquetas
ax.set_title("Figura 1.2: Anomalías promedio por estación (1880 - último año disponible)", fontsize=14)
ax.set_xlabel("Año")
ax.set_ylabel("Anomalía de temperatura (°C)")
ax.legend()
ax.grid(True, alpha=0.3)
# --- guardar figura 2 ---
filename = "anomalias_estaciones.png"
fig.savefig(figures_path / filename, dpi=300, bbox_inches="tight")
plt.close(fig)
#---------------------------------------------------------------------------------------------------------------
# --- construir gráfico iii)---
fig, ax = plt.subplots(figsize=(10, 6))
serie = df["J-D"].dropna()
ax.plot(serie.index, serie.values, color="black", linewidth=2, label="Promedio anual (J-D)")
# Línea horizontal en 0 con etiqueta
ax.axhline(0, color="blue", linestyle="--", linewidth=1)
ax.text(serie.index.min(), 0.05, "promedio de 1951 a 1980", color="blue", fontsize=9)
# Etiquetas y título
ax.set_title("Figura 1.3: Anomalías promedio anuales (J-D)", fontsize=14)
ax.set_xlabel("Año")
ax.set_ylabel("Anomalía de temperatura (°C)")
ax.legend()
ax.grid(True, alpha=0.3)
# --- guardar figura 3---
filename = "anomalias_anuales.png"
fig.savefig(figures_path / filename, dpi=300, bbox_inches="tight")
plt.close(fig)


#SEGUNDA SECCIÓN

#1.2.1 CREAR TABLAS DE FRECUENCIA
periodo1 = df.loc[1951:1980, "J-D"].dropna()
periodo2 = df.loc[1981:2010, "J-D"].dropna()
bins = np.arange(-1.0, 2.1, 0.2)  # de -1.0 a 2.0 en pasos de 0.2
tabla1 = pd.cut(periodo1, bins).value_counts().sort_index()
tabla2 = pd.cut(periodo2, bins).value_counts().sort_index()
frecuencias = pd.DataFrame({
    "1951–1980": tabla1,
    "1981–2010": tabla2
})
print(frecuencias)
# --- limpiar índices de los bins ---
frecuencias.index = [f"{i.left:.1f} a {i.right:.1f}" for i in frecuencias.index]
# --- exportar a LaTeX ---
latex_path = tables_path / "frecuencias_periodos.tex"
with open(latex_path, "w", encoding="utf-8") as f:
    f.write(frecuencias.to_latex(
        caption="Frecuencias de anomalías anuales de temperatura en dos periodos comparativos (1951--1980 y 1981--2010).",
        label="tab:frecuencias",
        index=True
    ))

print(f"Tabla guardada en: {latex_path}")

#1.2.2 HISTOGRAMAS
# --- gráfico ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Histograma 1951–1980
axes[0].hist(periodo1, bins=bins, color="skyblue", edgecolor="black")
axes[0].set_title("Distribución de anomalías (1951–1980)")
axes[0].set_xlabel("Anomalía de temperatura (°C)")
axes[0].set_ylabel("Frecuencia")

# Histograma 1981–2010
axes[1].hist(periodo2, bins=bins, color="salmon", edgecolor="black")
axes[1].set_title("Distribución de anomalías (1981–2010)")
axes[1].set_xlabel("Anomalía de temperatura (°C)")

plt.tight_layout()

# --- guardar figura ---
filename = "histogramas_periodos.png"
fig.savefig(figures_path / filename, dpi=300, bbox_inches="tight")
plt.close(fig)

#1.2.3 DECILES
q3 = np.quantile(periodo1, 0.3)  # 3er decil
q7 = np.quantile(periodo1, 0.7)  # 7mo decil
print("Decil 3 (30%):", q3)
print("Decil 7 (70%):", q7)

#1.2.4 Temperaturas calientes
calientes = (periodo2 >= 0.08).sum()
total = periodo2.shape[0]
porcentaje = 100 * calientes / total

print("Años calientes:", calientes)
print("Total años:", total)
print("Porcentaje de años calientes:", porcentaje)


#1.2.5 estadisticas descriptivas por nivel de años
periodos = {
    "1921–1950": df.loc[1921:1950, ["DJF", "MAM", "JJA", "SON"]],
    "1951–1980": df.loc[1951:1980, ["DJF", "MAM", "JJA", "SON"]],
    "1981–2010": df.loc[1981:2010, ["DJF", "MAM", "JJA", "SON"]],
}

# --- calcular medias y varianzas ---
resultados = {}
for nombre, datos in periodos.items():
    medias = datos.mean()
    varianzas = datos.var()
    resultados[nombre] = pd.DataFrame({
        "Media": medias.round(3),
        "Varianza": varianzas.round(3)
    })

tabla = pd.concat(resultados, axis=1)

# --- guardar como LaTeX ---
base_path = Path(r"C:\Users\Lenovo\Documents\Universidad\Material Clases\Haciendo Economía\Taller3")
tables_path = base_path / "Outputs" / "Tables"
tables_path.mkdir(parents=True, exist_ok=True)

latex_path = tables_path / "medias_varianzas.tex"
with open(latex_path, "w", encoding="utf-8") as f:
    f.write(tabla.to_latex(
        caption="Media y varianza de las anomalías de temperatura por estación y periodo.",
        label="tab:medias-varianzas",
        index=True,
        multirow=True
    ))

print(f"Tabla guardada en: {latex_path}")


#SECCIÓN 3
#1.3.3 GRAFICO DE TENDENCIA VS INTERPOLATED
# --- cargar datos ---
co2_file = rawdata_path / "Co2_Manu_loa.xlsx"
co2 = pd.read_excel(co2_file)
print(co2.head())
# --- crear columna de fecha ---
co2["Date"] = pd.to_datetime(dict(year=co2["Year"], month=co2["Month"], day=1))

# --- filtrar desde 1960 ---
co2 = co2[co2["Date"] >= "1960-01-01"]

# --- limpiar valores faltantes (-99.99) ---
co2 = co2.replace(-99.99, pd.NA)

# --- gráfico ---
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(co2["Date"], co2["Interpolated"], label="Interpolated (observado)", color="gray", alpha=0.6)
ax.plot(co2["Date"], co2["Trend"], label="Trend (suavizado)", color="red", linewidth=2)

ax.set_title("Figura 3.1: Concentración de CO$_2$ en Mauna Loa (1960–presente)", fontsize=14)
ax.set_xlabel("Año")
ax.set_ylabel("CO$_2$ (ppm)")
ax.legend()
ax.grid(True, alpha=0.3)

# --- guardar ---
filename = "co2_interpolated_trend.png"
fig.savefig(figures_path / filename, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"Gráfico guardado en: {figures_path / filename}")

#1.3.4 GRAFICO COMPARACION TEMPERATURA CO2
# --- 1. Filtrar marzo en el dataset de CO₂ ---
df_co2_mar = co2[co2["Month"] == 3][["Year", "Monthly average", "Trend"]]

# Limpiar valores faltantes (-99.99 en Mauna Loa)
df_co2_mar = df_co2_mar.replace(-99.99, pd.NA).dropna()

# --- 2. Combinar con anomalías de temperatura de marzo ---
df_temp_co2 = pd.merge(df_co2_mar, df.reset_index(), on="Year")

# Verificar primeras filas
print(df_temp_co2[["Year", "Mar", "Monthly average", "Trend"]].head())

# Diagrama de dispersión: temperatura en marzo vs CO₂ (tendencia)
fig, ax = plt.subplots(figsize=(7,5))
ax.scatter(df_temp_co2["Mar"], df_temp_co2["Trend"], color="darkred", alpha=0.7)

ax.set_title("CO$_2$ (Mauna Loa, tendencia) vs Anomalía de temperatura en marzo")
ax.set_xlabel("Anomalía de temperatura en marzo (°C)")
ax.set_ylabel("CO$_2$ (ppm)")
ax.grid(True, alpha=0.3)

# Guardar gráfico
filename = "dispersion_co2_mar.png"
fig.savefig(figures_path / filename, dpi=300, bbox_inches="tight")
plt.close(fig)

# --- 4. Correlación de Pearson ---
r, p = pearsonr(df_temp_co2["Mar"], df_temp_co2["Trend"])
print("Coeficiente de Pearson:", r)
print("Valor-p:", p)