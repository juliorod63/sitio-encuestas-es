import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import matplotlib.pyplot as plt


from utils import load_data, transformacion_df, calcular_NPS_Alexia, calcular_NPS_Servicio, calcular_CSAT,  calcular_CSAT_Capacitacion, transformar_cargos

#nlp = spacy.load("es_core_news_sm")

st.set_page_config(
    page_title="Resultados Encuesta Satisfacción Clientes España",
    page_icon=":bar_chart:",
    layout="wide"
)



st.title("Resultados Encuesta Satisfacción Clientes España")
st.write("Bienvenido a la aplicación de Resultados Encuesta Satisfacción Clientes España.")

password_guess = st.text_input("Ingrese la contraseña para acceder a los resultados:", type="password")

if password_guess != st.secrets["password"]:
   
    st.write("Contraseña incorrecta. Inténtalo de nuevo.")
    st.stop()
else:
    st.sidebar.header("Resultados de la Encuesta")

    st.sidebar.markdown("- [Resultados de la Encuesta](#resultados-de-la-encuesta)")
    st.sidebar.markdown("- [Métricas Clave](#metricas-clave)")
    st.sidebar.markdown("- [Matriz de Dispersión](#matriz-de-dispersion)")
    st.sidebar.markdown("- [Análisis de NPS por Variables](#analisis-de-nps-por-variables)")
    st.sidebar.markdown("- [Análisis de Respuestas por Centro](#analisis-de-respuestas-por-centro)")
    st.sidebar.markdown("- [Análisis Detallado NPS Recomendar por Centro](#analisis-detallado-nps-recomendar-por-centro)")
    st.sidebar.markdown("- [Análisis NPS y CSAT por Rol](#analisis-nps-y-csat-por-rol)")
    st.success("Contraseña correcta. Acceso concedido.")

#url del archivo
file_path = "https://raw.githubusercontent.com/juliorod63/DATASETS/refs/heads/main/ES-SatisfaccionAlexia2025..csv"
df = load_data(file_path)

st.markdown("### Resultados de la Encuesta")
st.write(" Respuestas: ", df.shape[0])


df = transformacion_df(df)
df = transformar_cargos(df)


st.dataframe(df)
st.header("Métricas Clave")

st.divider()
with st.expander("¿Cómo calculamos el NPS y el CSAT?"):

    st.markdown("""
    El NPS (Net Promoter Score) se calcula restando el porcentaje de detractores del porcentaje de promotores.
    **Fórmula:**
    ```python
    NPS = (Promotores - Detractores) / Total de respuestas × 100
    promoters = df[df["NPS_Servicio"] >= 9].shape[0]
    detractors = df[df["NPS_Servicio"] <= 6].shape[0]
    total = df["NPS_Servicio"].shape[0]
    nps = ((promoters - detractors) / total) * 100
   

    """)
    st.markdown("""
    El CSAT (Customer Satisfaction Score) se calcula como el porcentaje de respuestas positivas sobre el total de respuestas.
    **Fórmula:**
    ```python
    CSAT = (Respuestas positivas / Total de respuestas) × 100
    csat = (df["CS_Alexia"].isin([4, 5]).sum() / df["CS_Alexia"].count()) * 100
    """)

col1, col2, col3 = st.columns(3)
col1.metric(label="NPS Alexia", value=f"{calcular_NPS_Alexia(df):.2f}", help="NPS basado en la pregunta de recomendar Alexia")
col2.metric(label="NPS Servicio", value=f"{calcular_NPS_Servicio(df):.2f}", help="NPS basado en la pregunta de recomendar el Servicio")
col3.metric(label="CSAT", value=f"{calcular_CSAT(df):.2f}", help="CSAT basado en la satisfacción con Alexia")


st.divider()


st.plotly_chart(px.histogram(df, x="NPS_Servicio", color="Cargo", title="Distribución de NPS x Cargo"))

st.plotly_chart(px.histogram(df, x="NPS_Servicio", color="Skil", title="Distribución de NPS x Skill"))

st.plotly_chart(px.histogram(df, x="Satisfaccion_Alexia", color="PROVINCIA", title="Distribución de CSAT x Provincia"))

st.plotly_chart(px.histogram(df, x="NPS_Alexia", color="Skil", title="Distribución x NPS Alexia x Skill"))

st.plotly_chart(px.histogram(df, x="NPS_Alexia", color="Antiguedad", title="Distribución por NPS Alexia y Antiguedad"))



# Selecciona las columnas numéricas que quieres comparar
cols = ["Satisfaccion_Alexia", "NPS_Alexia", "NPS_Servicio"]  # ajusta según tus datos

st.markdown("### Matriz de Dispersión")
fig = ff.create_scatterplotmatrix(df[cols], diag='box',height=800, width=800)
st.plotly_chart(fig, use_container_width=True)



st.markdown("### Análisis de NPS por Variables")
# Supón que df es tu DataFrame ya cargado y transformado
variables = ["Cargo", "Antiguedad", "Centro", "Modulo_Usado", "Skil"]  # agrega las variables que quieras analizar

opcion = st.selectbox("Selecciona una variable para analizar NPS_Recomendacion:", variables)

# Gráfico de distribución de NPS_Recomendacion según la variable seleccionada
fig = px.violin(df, x=opcion, y="NPS_Alexia", title=f"NPS Alexia según {opcion}")
st.plotly_chart(fig)

# Gráfico de distribución de NPS_Recomendacion según la variable seleccionada
fig = px.violin(df, x=opcion, y="NPS_Servicio", title=f"NPS Servicio según {opcion}")
st.plotly_chart(fig)


fig = px.violin(df, x=opcion, y="Satisfaccion_Alexia", title=f"Satisfaccion Alexia según {opcion}")
st.plotly_chart(fig)

st.markdown("### Análisis de Respuestas por Centro")

centros_count = df["Centro"].value_counts().reset_index()
centros_count.columns = ["Centro", "Respuestas"]

st.metric(label="Centros", value=f"{centros_count.shape[0]}")

fig = px.bar(centros_count, x="Centro", y="Respuestas", title="Cantidad de respuestas por Centro")
st.plotly_chart(fig)

# calcular_NPS_Alexia recibe un DataFrame y calcula el NPS
tabla_nps = df.groupby("Centro", group_keys=False).apply(calcular_NPS_Alexia).reset_index()
tabla_nps.columns = ["Centro", "NPS_Alexia"]


fig = px.bar(tabla_nps, x="Centro", y="NPS_Alexia", title="NPS Alexia por Centro")
st.plotly_chart(fig)

st.markdown("### Análisis Detallado NPS Recomendar por Centro")
# Selector de centro
centros_ordenados = sorted(df["Centro"].unique())
centro_seleccionado = st.selectbox("Selecciona un centro:", centros_ordenados)

# Filtra el DataFrame por el centro seleccionado
df_filtrado = df[df["Centro"] == centro_seleccionado]
st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Respuestas", value=f"{df_filtrado.shape[0]}")
col2.metric(label="NPS Alexia", value=f"{calcular_NPS_Alexia(df_filtrado):.2f}")
col3.metric(label="CSAT", value=f"{calcular_CSAT(df_filtrado):.2f}")
col4.metric(label="NPS Servicio", value=f"{calcular_NPS_Servicio(df_filtrado):.2f}")

# Grafica la distribución de NPS_Alexia para ese centro
fig = px.histogram(df_filtrado, x="NPS_Alexia", nbins=10, range_x=[1,10],title=f"Distribución de NPS_Alexia en {centro_seleccionado}")
st.plotly_chart(fig)

fig = px.histogram(df_filtrado, x="NPS_Servicio", nbins=10, range_x=[1,10], title=f"Distribución de NPS_Servicio en {centro_seleccionado}")
st.plotly_chart(fig)

fig = px.histogram(df_filtrado, x="Satisfaccion_Alexia", nbins=10, range_x=[1,5], title=f"Distribución de CSAT en {centro_seleccionado}")
st.plotly_chart(fig)


st.markdown("### NPS_Alexia por Centro")
st.dataframe(tabla_nps)

st.markdown("### Análisis NPS y CSAT por Rol"  )
tabla_nps_rol = df.groupby("Cargo", group_keys=False).apply(calcular_NPS_Alexia).reset_index()
tabla_nps_rol.columns = ["Cargo", "NPS_Alexia"]

fig = px.bar(tabla_nps_rol, x="Cargo", y="NPS_Alexia", title="NPS Alexia por Cargo")
st.plotly_chart(fig)

tabla_csat_rol = df.groupby("Cargo", group_keys=False).apply(calcular_CSAT).reset_index()
tabla_csat_rol.columns = ["Cargo", "Satisfaccion_Alexia"]

fig = px.bar(tabla_csat_rol, x="Cargo", y="Satisfaccion_Alexia", title="Satisfaccion Alexia por Cargo")
st.plotly_chart(fig)

# Agrupar y calcular promedio CSAT
df_burbujas = df.groupby(['Cargo', 'Antiguedad'], as_index=False)['Satisfaccion_Alexia'].mean()
df_burbujas.rename(columns={'Satisfaccion_Alexia': 'CSAT_promedio'}, inplace=True)

fig = px.scatter(
    df_burbujas,
    x='Cargo',
    y='Antiguedad',
    size='CSAT_promedio',
    color='Cargo',
    title='CSAT promedio por Cargo y Antigüedad',
    size_max=40
)
fig.update_xaxes(type='category')
st.plotly_chart(fig)

