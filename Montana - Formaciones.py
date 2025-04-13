import streamlit as st

# --- DATOS DE JUGADORES ---
all_players = {
    "A": ["Axel"],  # Arqueros
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

st.set_page_config(layout="wide")
st.title("⚽ Organizador de Formaciones con Máxima Flexibilidad")

# 1) Elegir cuántos jugadores de campo (excluyendo arquero)
num_players = st.number_input(
    "Número de jugadores de campo (excl. arquero)",
    min_value=0, max_value=10, value=5
)

# 2) Definir cuántos serán Defensas, Mediocampistas y Delanteros
st.subheader("Distribución de Jugadores en la Cancha")
def_col, mid_col, fwd_col = st.columns(3)

with def_col:
    num_def = st.number_input(
        "Defensas",
        min_value=0, max_value=num_players, value=2
    )
with mid_col:
    num_mid = st.number_input(
        "Mediocampistas",
        min_value=0, max_value=num_players, value=2
    )
with fwd_col:
    num_fwd = st.number_input(
        "Delanteros",
        min_value=0, max_value=num_players, value=1
    )

# Validamos que la suma de D+M+F coincida con el total elegido
if (num_def + num_mid + num_fwd) != num_players:
    st.error(f"La suma (D+M+F) debe ser igual a {num_players}. Corrígelo para continuar.")
    st.stop()

# 3) Seleccionar manualmente cada jugador para cada línea
st.markdown("---")
st.subheader("Asignación de Jugadores a Posiciones")

defender_choices = []
mid_choices = []
fwd_choices = []

# --- DEFENSAS ---
if num_def > 0:
    st.markdown("#### Defensas")
    cols_def = st.columns(num_def)
    for i in range(num_def):
        with cols_def[i]:
            player = st.selectbox(
                f"Defensa {i+1}",
                options=["(Ninguno)"] + all_players["D"],
                key=f"def_{i}"  # Para que no choquen los keys
            )
            defender_choices.append(player)

# --- MEDIOCAMPISTAS ---
if num_mid > 0:
    st.markdown("#### Mediocampistas")
    cols_mid = st.columns(num_mid)
    for i in range(num_mid):
        with cols_mid[i]:
            player = st.selectbox(
                f"Mediocampista {i+1}",
                options=["(Ninguno)"] + all_players["M"],
                key=f"mid_{i}"
            )
            mid_choices.append(player)

# --- DELANTEROS ---
if num_fwd > 0:
    st.markdown("#### Delanteros")
    cols_fwd = st.columns(num_fwd)
    for i in range(num_fwd):
        with cols_fwd[i]:
            player = st.selectbox(
                f"Delantero {i+1}",
                options=["(Ninguno)"] + all_players["F"],
                key=f"fwd_{i}"
            )
            fwd_choices.append(player)

# 4) Mostrar Arquero Fijo y DT
st.markdown("#### Arquero")
st.write(all_players["A"][0])

st.markdown("#### DT")
st.write(all_players["DT"][0])

# --- VISUALIZACIÓN FINAL TIPO “CANCHA” ---
st.markdown("---")
st.markdown("## Visualización en la Cancha")

# Para simular un layout “tipo FIFA”, mostramos:
# Forwards (arriba) -> Midfielders (medio) -> Defenders (abajo) -> GK

# --- DELANTEROS ---
if num_fwd > 0:
    st.markdown("#### Delanteros (arriba)")
    row_forwards = st.columns(num_fwd)
    for i, fwd_name in enumerate(fwd_choices):
        row_forwards[i].markdown(f"**{fwd_name}**")

# --- MEDIOCAMPISTAS ---
if num_mid > 0:
    st.markdown("#### Mediocampistas (centro)")
    row_mids = st.columns(num_mid)
    for i, mid_name in enumerate(mid_choices):
        row_mids[i].markdown(f"**{mid_name}**")

# --- DEFENSAS ---
if num_def > 0:
    st.markdown("#### Defensas (abajo)")
    row_defs = st.columns(num_def)
    for i, def_name in enumerate(defender_choices):
        row_defs[i].markdown(f"**{def_name}**")

# --- ARQUERO ---
st.markdown("#### Arquero (última línea)")
st.markdown(f"**{all_players['A'][0]}**")
