import streamlit as st

# Datos
all_players = {
    "A": ["Axel"],
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

formations = {
    4: [[2, 1, 1], [1, 2, 1]],
    5: [[2, 2, 1], [1, 2, 2]],
    6: [[2, 3, 1], [3, 2, 1], [2, 2, 2]],
    7: [[3, 3, 1], [2, 3, 2], [3, 2, 2]],
    8: [[4, 3, 1], [3, 3, 2], [3, 2, 3]],
    9: [[4, 4, 1], [3, 4, 2], [3, 3, 3]],
    10: [[4, 4, 2], [3, 4, 3]],
}

st.set_page_config(layout="wide")
st.title("⚽ Organizador de Formaciones")

# Selección de cantidad y formación
num_players = st.selectbox("Cantidad de jugadores (sin contar arquero)", list(formations.keys()))
formation_list = formations[num_players]
formation = st.selectbox("Formación (Defensa - Medio - Ataque)", formation_list)

# Selección automática de jugadores
outfield = all_players["D"] + all_players["M"] + all_players["F"]
selected = outfield[:num_players]
bench = outfield[num_players:num_players + 5]

defenders = selected[:formation[0]]
midfielders = selected[formation[0]:formation[0]+formation[1]]
forwards = selected[formation[0]+formation[1]:]

# Layout cancha + banco
col_cancha, col_banco = st.columns([4, 1])

with col_cancha:
    st.markdown("### 🏟️ Cancha")
    st.markdown(f"**Formación:** {formation[0]} - {formation[1]} - {formation[2]}")

    # Delanteros
    st.markdown("#### 🔥 Delanteros")
    cols = st.columns(formation[2])
    for i, p in enumerate(forwards):
        cols[i].markdown(f"**{p}**")

    # Mediocampistas
    st.markdown("#### 🎯 Mediocampistas")
    cols = st.columns(formation[1])
    for i, p in enumerate(midfielders):
        cols[i].markdown(f"**{p}**")

    # Defensores
    st.markdown("#### 🛡️ Defensores")
    cols = st.columns(formation[0])
    for i, p in enumerate(defenders):
        cols[i].markdown(f"**{p}**")

    # Arquero
    st.markdown("#### 🧤 Arquero")
    st.markdown(f"**{all_players['A'][0]}**")

with col_banco:
    st.markdown("### 🪑 Suplentes")
    for p in bench:
        st.write(p)

    st.markdown("### 🎩 DT")
    st.write(all_players["DT"][0])
