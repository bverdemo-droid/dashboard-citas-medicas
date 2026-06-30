import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página con estilo limpio
st.set_page_config(
    page_title="Analytics | Hospital Lima Norte", 
    layout="wide", 
    page_icon="🏥"
)

# Estilo CSS personalizado para mejorar la tipografía y los bordes
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1 {color: #1E3A8A; font-weight: 700;}
    h3 {color: #4B5563;}
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado Corporativo
st.title('🏥 Plataforma Inteligente de Gestión de Citas')
st.markdown('**Hospital de Lima Norte** | Dirección de Operaciones y BI')
st.markdown("---")
# 3. Carga y preparación optimizada de datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv('citas_medicas.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Diccionario para transformar números de mes a etiquetas elegantes
    meses_dict = {
        1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
        7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'
    }
    df['mes_num'] = df['fecha'].dt.month
    df['mes_nom'] = df['mes_num'].map(meses_dict)
    return df

df = cargar_datos()

# ==========================================
# SECCIÓN DE KPIs (MÉTRICAS CLAVE)
# ==========================================
total_citas = len(df)
atendidas = len(df[df['estado'] == 'Atendida'])
tasa_asistencia = (atendidas / total_citas) * 100
canceladas_ausentes = len(df[df['estado'].isin(['Cancelada', 'No asistió'])])

# Estructura de 3 columnas para los indicadores principales
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Total General de Citas", value=f"{total_citas:,}")
with kpi2:
    st.metric(label="Tasa de Eficiencia (Atendidas)", value=f"{tasa_asistencia:.1f}%")
with kpi3:
    st.metric(label="Citas Pérdidas (Canceladas/Ausentes)", value=f"{canceladas_ausentes:,}", delta=f"-{(canceladas_ausentes/total_citas)*100:.1f}% de capacidad", delta_color="inverse")

st.markdown("---")

# ==========================================
# SECCIÓN DE GRÁFICOS PRINCIPALES
# ==========================================
col1, col2 = st.columns([6, 4])  # Distribución de tamaño proporcional (60% y 40%)

with col1:
    st.subheader('📌 Distribución de la Demanda por Especialidad')
    df_especialidad = df['especialidad'].value_counts().reset_index()
    df_especialidad.columns = ['Especialidad', 'Cantidad']
    
    # Gráfico de barras horizontal para mayor elegancia y lectura de nombres
    fig1 = px.bar(
        df_especialidad, 
        x='Cantidad', 
        y='Especialidad', 
        orientation='h',
        text_auto=True,
        color='Cantidad',
        color_continuous_scale='Blues' # Escala monocromática azul profesional
    )
    fig1.update_layout(
        showlegend=False, 
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader('📊 Estado Operativo de Citas')
    
    # Paleta de colores específica para el sector salud (Éxito, Alerta, Danger)
    colores_estado = {
        'Atendida': '#1E40AF',   # Azul corporativo
        'Cancelada': '#9CA3AF',  # Gris neutro
        'No asistió': '#EF4444'  # Rojo alerta
    }
    
    fig2 = px.pie(
        df, 
        names='estado', 
        hole=0.5, # Transforma el gráfico de pastel a un moderno gráfico de dona
        color='estado',
        color_discrete_map=colores_estado
    )
    fig2.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# SECCIÓN DE TENDENCIA TEMPORAL
# ==========================================
st.markdown("---")
st.subheader('📈 Evolución Cronológica Mensual de Citas')

# Agrupamos y ordenamos correctamente por número de mes, pero mostramos el nombre
citas_mes = df.groupby(['mes_num', 'mes_nom']).size().reset_index(name='cantidad').sort_values(by='mes_num')

fig3 = px.line(
    citas_mes, 
    x='mes_nom', 
    y='cantidad', 
    markers=True,
    labels={'mes_nom': 'Mes', 'cantidad': 'Volumen de Citas'}
)
fig3.update_traces(
    line_color='#1D4ED8', 
    line_width=3, 
    marker=dict(size=8, color='#1E3A8A', symbol='circle')
)
fig3.update_layout(
    plot_bgcolor='rgba(243,244,246,0.5)', # Fondo grisáceo sumamente sutil
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#E5E7EB'),
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig3, use_container_width=True)
