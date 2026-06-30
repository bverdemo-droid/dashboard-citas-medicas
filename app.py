import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Citas Médicas", layout="wide", page_icon="🏥")

st.title('🏥 Dashboard de Gestión de Citas Médicas')
st.markdown('### Hospital de Lima Norte - Análisis de Indicadores Clave')

@st.cache_data
def cargar_datos():
    df = pd.read_csv('citas_medicas.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    return df

df = cargar_datos()

col1, col2 = st.columns(2)

with col1:
    st.subheader('📌 Citas por Especialidad')
    df_especialidad = df['especialidad'].value_counts().reset_index()
    df_especialidad.columns = ['Especialidad', 'Cantidad']
    fig1 = px.bar(df_especialidad, x='Especialidad', y='Cantidad', color='Especialidad', text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader('📊 Estado de las Citas')
    fig2 = px.pie(df, names='estado', color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader('📈 Tendencia Mensual de Citas Médicas')
citas_mes = df.groupby('mes').size().reset_index(name='cantidad').sort_values(by='mes')
fig3 = px.line(citas_mes, x='mes', y='cantidad', markers=True, labels={'mes': 'Mes del Año', 'cantidad': 'Total de Citas'})
st.plotly_chart(fig3, use_container_width=True)
