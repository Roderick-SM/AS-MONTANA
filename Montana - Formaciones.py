# formation_app.py
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

num_players = st.selectbox("Cantidad de jugadores (sin contar arquero)", list(formations.keys()))
formation_list = formations[num_players]
formation = st.selectbox("Formación (Defensa-Medio-Ataque)", formation_list)

# Selección automática
outfield = all_players["D"] + all_players["M"] + all_players["F"]
selected = outfield[:num_players]
bench = outfield[num_players:num_players + 5]
reserves = outfield[num_players + 5:]

defenders = selected[:formation[0]]
midfielders = selected[formation[0]:formation[0]+formation[1]]
forwards = selected[formation[0]+formation[1]:]

# Mostrar cancha
st.subheader("📋 Formación en cancha")
st.markdown("Arquero: **{}**".format(all_players["A"][0]))

col1, col2, col3 = st.columns(3)
col1.markdown("### 🛡️ Defensores")
for p in defenders:
    col1.write(p)

col2.markdown("### 🎯 Mediocampistas")
for p in midfielders:
    col2.write(p)

col3.markdown("### 🔥 Delanteros")
for p in forwards:
    col3.write(p)

# Mostrar banco
st.subheader("🪑 Banco de suplentes")
for p in bench:
    st.write(p)

# Reserva
st.subheader("📋 Jugadores en reserva")
for p in reserves:
    st.write(p)

# DT
st.subheader("🎩 DT")
st.write(all_players["DT"][0])
