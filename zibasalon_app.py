import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración inicial
st.set_page_config(page_title="AVYNA SALON ZIBATA Agenda", page_icon="✂️", layout="wide")

# Estilos personalizados: fondo oscuro con colores ZIBA
st.markdown("""
    <style>
        body, .stApp {
            background-color: #111111;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #ffcc00;
            color: black;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.4em 1em;
        }
        .stDataFrame {
            background-color: #222222;
        }
        .e1fqkh3o3 {
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ ZIBA SALÓN - Agenda y Recompensas 💛🖤")

# Inicialización de datos
if "citas" not in st.session_state:
    st.session_state.citas = []

if "rewards" not in st.session_state:
    st.session_state.rewards = {}

# Servicios del salón
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

# Sección para agendar nuevas citas
st.header("📅 Registrar nueva cita")
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre del cliente")
    servicio = st.selectbox("Servicio", list(servicios.keys()))
    fecha = st.date_input("Fecha de la cita", value=datetime.now())
    hora = st.time_input("Hora", value=datetime.now().time())

with col2:
    if st.button("Agregar cita"):
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
        st.session_state.rewards[nombre] = st.session_state.rewards.get(nombre, 0) + recompensa
        st.success(f"Cita registrada para {nombre}. Ganó {recompensa} ZRS 🎉")

# Mostrar citas actuales con botones
st.header("📋 Agenda actual")
if st.session_state.citas:
    for i, cita in enumerate(st.session_state.citas):
        cols = st.columns([2, 2, 2, 2, 2, 1, 1])
        cols[0].write(cita["Nombre"])
        cols[1].write(cita["Servicio"])
        cols[2].write(cita["Fecha"])
        cols[3].write(cita["Hora"])
        cols[4].write(f"${cita['Precio']} / {cita['ZIBA REWARDS']} ZRS")
        
        if cols[5].button("✏️ Editar", key=f"edit_{i}"):
            st.session_state.edit_index = i
        if cols[6].button("❌ Cancelar", key=f"cancel_{i}"):
            st.session_state.rewards[cita["Nombre"]] -= cita["ZIBA REWARDS"]
            st.session_state.citas.pop(i)
            st.experimental_rerun()

    # Formulario para editar cita
    if "edit_index" in st.session_state:
        st.subheader("Editar cita")
        idx = st.session_state.edit_index
        cita = st.session_state.citas[idx]
        new_nombre = st.text_input("Nuevo nombre", value=cita["Nombre"], key="edit_nombre")
        new_servicio = st.selectbox("Nuevo servicio", list(servicios.keys()), index=list(servicios.keys()).index(cita["Servicio"]), key="edit_servicio")
        new_fecha = st.date_input("Nueva fecha", value=datetime.strptime(cita["Fecha"], "%Y-%m-%d"), key="edit_fecha")
        new_hora = st.time_input("Nueva hora", value=datetime.strptime(cita["Hora"], "%H:%M").time(), key="edit_hora")

        if st.button("Guardar cambios"):
            precio_nuevo = servicios[new_servicio]
            recompensa_nueva = round(precio_nuevo * 0.10, 2)
            # Ajustar recompensas
            st.session_state.rewards[cita["Nombre"]] -= cita["ZIBA REWARDS"]
            st.session_state.rewards[new_nombre] = st.session_state.rewards.get(new_nombre, 0) + recompensa_nueva
            # Actualizar cita
            st.session_state.citas[idx] = {
                "Nombre": new_nombre,
                "Servicio": new_servicio,
                "Fecha": new_fecha.strftime("%Y-%m-%d"),
                "Hora": new_hora.strftime("%H:%M"),
                "Precio": precio_nuevo,
                "ZIBA REWARDS": recompensa_nueva
            }
            del st.session_state["edit_index"]
            st.success("Cita actualizada correctamente")
            st.experimental_rerun()

else:
    st.info("No hay citas registradas aún.")

# Corte del día
st.header("📊 Corte del día")
hoy = datetime.now().strftime("%Y-%m-%d")
citas_hoy = [c for c in st.session_state.citas if c["Fecha"] == hoy]
if citas_hoy:
    total_ingresos = sum(c["Precio"] for c in citas_hoy)
    total_rewards = sum(c["ZIBA REWARDS"] for c in citas_hoy)
    st.markdown(f"🗓️ Fecha: **{hoy}**")
    st.markdown(f"💰 Total ingresos del día: **${total_ingresos}**")
    st.markdown(f"🎁 Total ZIBA REWARDS entregados: **{total_rewards} ZRS**")
    st.dataframe(pd.DataFrame(citas_hoy))
else:
    st.info("No hay citas registradas hoy.")

# Recompensas totales
st.header("💰 Recompensas acumuladas")
if st.session_state.rewards:
    df_rewards = pd.DataFrame(list(st.session_state.rewards.items()), columns=["Cliente", "ZIBA REWARDS (ZRS)"])
    st.dataframe(df_rewards)
else:
    st.info("Aún no hay recompensas registradas.")

st.markdown("---")
st.markdown("Desarrollado para AVYNA SALON ZIBATA ✂️ | ZIBA REWARDS 💛🖤")
