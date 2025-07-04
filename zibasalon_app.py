import streamlit as st
import pandas as pd
from datetime import datetime

# Estilo personalizado ZIBA (amarillo y negro)
st.set_page_config(page_title="ZIBA SALÓN Agenda", page_icon="✂️", layout="wide")
st.markdown("""
    <style>
        body { background-color: #fffbe6; }
        .stApp { background-color: #fffbe6; }
        h1, h2, h3, h4, h5, h6, .st-bx { color: #000000; }
        .css-18e3th9 { background-color: #fffbe6 !important; }
        .stButton>button { background-color: #ffcc00; color: black; font-weight: bold; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("💛🖤 ZIBA SALÓN - Agenda y Recompensas")

# Base de datos simulada
if "citas" not in st.session_state:
    st.session_state.citas = []

if "rewards" not in st.session_state:
    st.session_state.rewards = {}

# Servicios del salón (se puede modificar o ampliar)
servicios = {
    "Corte dama": 250,
    "Corte caballero": 200,
    "Alaciado exprés": 350,
    "Alaciado permanente": 800,
    "Tinte raíz": 400,
    "Tinte completo": 600,
    "Tratamiento capilar": 300,
    "Peinado": 350,
    "Uñas gelish": 300
}

# Sección: Registrar nueva cita
st.header("➕ Registrar nueva cita")

col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre del cliente")
    servicio = st.selectbox("Servicio", list(servicios.keys()))
    fecha = st.date_input("Fecha de la cita")
    hora = st.time_input("Hora")

with col2:
    registrar = st.button("📅 Agendar cita")
    if registrar and nombre:
        precio = servicios[servicio]
        recompensa = round(precio * 0.10, 2)
        cita = {
            "Nombre": nombre,
            "Servicio": servicio,
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Hora": hora.strftime("%H:%M"),
            "Precio": precio,
            "ZIBA REWARDS": recompensa
        }
        st.session_state.citas.append(cita)

        if nombre in st.session_state.rewards:
            st.session_state.rewards[nombre] += recompensa
        else:
            st.session_state.rewards[nombre] = recompensa

        st.success(f"Cita registrada para {nombre}. Ganó {recompensa} ZRS 🎉")

# Sección: Ver agenda
st.header("📋 Agenda actual")
if st.session_state.citas:
    df_citas = pd.DataFrame(st.session_state.citas)
    st.dataframe(df_citas)
else:
    st.info("Aún no hay citas registradas.")

# Sección: Historial de recompensas
st.header("💰 Historial de ZIBA REWARDS")
if st.session_state.rewards:
    df_rewards = pd.DataFrame(list(st.session_state.rewards.items()), columns=["Cliente", "ZIBA REWARDS (ZRS)"])
    st.dataframe(df_rewards)
else:
    st.info("Aún no hay recompensas registradas.")

# Footer
st.markdown("---")
st.markdown("Desarrollado para ZIBA SALÓN ✂️ | ZIBA REWARDS 💛🖤")
