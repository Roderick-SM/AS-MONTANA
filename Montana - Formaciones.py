import streamlit as st

# --- DATOS DE JUGADORES ---
all_players = {
    "A": ["Axel"],  # Arqueros
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

# Formaciones = cantidad de defensas, mediocampistas, delanteros
formations = {
    (4,3,3): "4-3-3",
    (4,4,2): "4-4-2",
    (3,5,2): "3-5-2",
    (3,4,3): "3-4-3",
    (5,3,2): "5-3-2",
    (2,3,1): "2-3-1",  # para 6 jugadores + arquero
    (2,2,2): "2-2-2",  # etc.
    # Agrega las formaciones que quieras
}

st.set_page_config(layout="wide")
st.title("⚽ Organizador de Formaciones con Selección Manual")

# 1) Elegir cantidad de jugadores (excl. arquero)
#    Filtramos sólo las formaciones que sumen esa cantidad
num_players = st.slider("Cantidad de jugadores de campo (excluyendo arquero)", 
                        min_value=4, max_value=10, value=6)

valid_formations = {
    k: v for k, v in formations.items() if sum(k) == num_players
}

if not valid_formations:
    st.warning("No hay formaciones predefinidas que coincidan con ese número de jugadores")
    st.stop()

# 2) Elegir una de las formaciones disponibles
formation_key = st.selectbox(
    "Elige formación (Defensas-Medios-Delanteros)",
    list(valid_formations.keys()),
    format_func=lambda k: valid_formations[k]
)

num_defenders, num_mids, num_forwards = formation_key

# --- Sección para “disponibilidad manual” ---
st.markdown("### Selección de Jugadores por Posición")

# Recuperamos la lista de defensores, mediocampistas y delanteros
defenders_available = all_players["D"]
mids_available = all_players["M"]
forwards_available = all_players["F"]

# Con Streamlit, si queremos evitar que el usuario repita jugadores, debemos controlar un set
# o marcarlos como “usados”. Ejemplo sencillo: no dejamos que se repitan, pero no lo forzamos
# (cada selectbox mostrará TODOS los jugadores de esa categoría). 
# Para hacerlo sin repetir, habría que programar más lógica con st.session_state.

chosen_defenders = []
chosen_mids = []
chosen_forwards = []

st.subheader("Defensas")
def_col = st.columns(num_defenders)
for i in range(num_defenders):
    with def_col[i]:
        d = st.selectbox(
            f"Defensa {i+1}",
            options=["(ninguno)"] + defenders_available
        )
        chosen_defenders.append(d)

st.subheader("Mediocampistas")
mid_col = st.columns(num_mids)
for i in range(num_mids):
    with mid_col[i]:
        m = st.selectbox(
            f"Mediocampista {i+1}",
            options=["(ninguno)"] + mids_available
        )
        chosen_mids.append(m)

st.subheader("Delanteros")
fwd_col = st.columns(num_forwards)
for i in range(num_forwards):
    with fwd_col[i]:
        fwd = st.selectbox(
            f"Delantero {i+1}",
            options=["(ninguno)"] + forwards_available
        )
        chosen_forwards.append(fwd)

# 3) Mostrar al arquero
st.markdown("### Arquero")
st.write(all_players["A"][0])

# 4) DT (opcional)
st.markdown("### DT")
st.write(all_players["DT"][0])

# --- Sección final con Resumen Visual ---
st.markdown("---")
st.markdown("## Resumen de la Formación")
st.write(f"Formación: **{valid_formations[formation_key]}**  \n"
         f"Defensas: {chosen_defenders}  \n"
         f"Mediocampistas: {chosen_mids}  \n"
         f"Delanteros: {chosen_forwards}  \n"
         f"Arquero: {all_players['A'][0]}  \n"
         f"DT: {all_players['DT'][0]}")

# Banco (jugadores que no asigné, si querés)
# Ejemplo: sacamos de la lista total los que elegimos para titular
# O generamos una lista con los no seleccionados
# Para simplificar, lo omitimos acá o lo hacemos con sets.
