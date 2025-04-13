import streamlit as st
import streamlit.components.v1 as components

# --------------------------
# 1. DATOS DE JUGADORES
# --------------------------
all_players = {
    "A": ["Axel"],  # Arquero
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

st.set_page_config(layout="wide")
st.title("AS Montana - Squad")

# --------------------------
# 2. CONFIGURACIÓN DE LA FORMACIÓN
# --------------------------
st.header("Configuración de la Formación")

num_players = st.number_input(
    "Número de jugadores de campo (excluyendo arquero)",
    min_value=0, max_value=10, value=5, step=1
)

# Elegir cuántos serán defensas, mediocampistas y delanteros.
col_dist = st.columns(3)
with col_dist[0]:
    num_def = st.number_input("Defensas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[1]:
    num_mid = st.number_input("Mediocampistas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[2]:
    num_fwd = st.number_input("Delanteros", min_value=0, max_value=num_players, value=1, step=1)

if (num_def + num_mid + num_fwd) != num_players:
    st.error(f"La suma (Defensas + Mediocampistas + Delanteros) debe ser igual a {num_players}.")
    st.stop()

# --------------------------
# 3. ASIGNACIÓN MANUAL DE JUGADORES A LA CANCHA
# --------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

# Para cada categoría se crea un selectbox cuyos ítems se van filtrando para evitar repeticiones.
def select_players(cat_key, num, key_prefix):
    choices = []
    if num > 0:
        st.subheader(f"{cat_key} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
            # De la lista original de esa categoría, removemos lo ya elegido.
            available = ["(Ninguno)"] + [p for p in all_players[cat_key] if p not in choices]
            with cols[i]:
                sel = st.selectbox(f"{cat_key} {i+1}", available, key=f"{key_prefix}_{i}")
            choices.append(sel)
    return choices

defender_choices = select_players("D", num_def, "def")
mid_choices      = select_players("M", num_mid, "mid")
fwd_choices      = select_players("F", num_fwd, "fwd")

st.markdown("#### Arquero")
arquero = all_players["A"][0]
st.write(f"**{arquero}**")

st.markdown("#### DT")
dt = all_players["DT"][0]
st.write(f"**{dt}**")

# --------------------------
# 4. VISUALIZACIÓN DE LA CANCHA
# --------------------------
st.markdown("---")
st.header("Visualización en la Cancha")

# Queremos una cancha con orientación vertical:
# - Delanteros en la parte superior
# - Mediocampistas en el centro
# - Defensas en la parte inferior
# - Arquero al final

def get_row_html(players, top_pct):
    """Genera HTML para una fila (horizontal) de jugadores, distribuidos según el ancho."""
    html = ""
    valid = [p for p in players if p != "(Ninguno)"]
    if valid:
        n = len(valid)
        for i, player in enumerate(valid):
            left_pct = (i + 1) / (n + 1) * 100
            html += f"""
            <div style="position: absolute; top: {top_pct}%; left: {left_pct}%;
                        transform: translate(-50%, -50%); text-align: center;">
                <div style="font-size: 36px; color: #fff;">●</div>
                <div style="font-size: 22px; font-weight: bold; color: #fff;">{player}</div>
            </div>
            """
    return html

# Asignamos porcentajes verticales para cada línea:
top_forwards   = 20   # Delanteros (arriba)
top_midfield   = 45   # Mediocampistas (centro)
top_defense    = 70   # Defensas (abajo)
top_goalkeeper = 90   # Arquero (más abajo)

html_forwards = get_row_html(fwd_choices, top_forwards)
html_midfield = get_row_html(mid_choices, top_midfield)
html_defense  = get_row_html(defender_choices, top_defense)
html_goalkeeper = f"""
<div style="position: absolute; top: {top_goalkeeper}%; left: 50%;
            transform: translate(-50%, -50%); text-align: center;">
    <div style="font-size: 36px; color: #fff;">●</div>
    <div style="font-size: 22px; font-weight: bold; color: #fff;">{arquero}</div>
</div>
"""

# La cancha:
field_width = 800
field_height = 550
# Fondo: verde uniforme, con línea central horizontal y círculo central.
html_field = f"""
<div style="position: relative; width: {field_width}px; height: {field_height}px;
         background-color: #1e7d36; border: 2px solid #000; margin-bottom: 20px;">
    <!-- Línea central horizontal -->
    <div style="position: absolute; top: {field_height/2}px; left: 0; width: 100%; height: 2px; background: white;"></div>
    <!-- Círculo central -->
    <div style="position: absolute; left: 50%; top: 50%; width: 80px; height: 80px; margin-left: -40px; margin-top: -40px;
         border: 2px solid white; border-radius: 50%;"></div>
    {html_forwards}
    {html_midfield}
    {html_defense}
    {html_goalkeeper}
</div>
"""

components.html(html_field, height=field_height + 40)

# --------------------------
# 5. SUPLENTES Y RESERVAS
# --------------------------
st.markdown("---")
st.header("Suplentes y Reservas")

# En la columna derecha (separada de la cancha) se permiten elegir manualmente los suplentes.
# Disponemos las opciones para cada categoría (D, M, F) tomando de la lista original aquellos que no fueron usados en cancha.
col_dummy, col_banco = st.columns([2, 1])

with col_banco:
    st.subheader("Suplentes")
    bench_def = st.multiselect(
        "Suplentes - Defensas",
        options=[p for p in all_players["D"] if p not in defender_choices]
    )
    bench_mid = st.multiselect(
        "Suplentes - Mediocampistas",
        options=[p for p in all_players["M"] if p not in mid_choices]
    )
    bench_fwd = st.multiselect(
        "Suplentes - Delanteros",
        options=[p for p in all_players["F"] if p not in fwd_choices]
    )
    st.markdown("**DT**")
    st.write(dt)
    
    st.markdown("---")
    st.subheader("Reservas")
    # Calculamos los jugadores del outfield (D, M, F) que no estén ni en cancha ni elegidos como suplentes.
    used = set(defender_choices + mid_choices + fwd_choices + bench_def + bench_mid + bench_fwd)
    all_outfield = set(all_players["D"] + all_players["M"] + all_players["F"])
    reserves = sorted(list(all_outfield - used))
    # Se muestran en un multiselect para referencia (aunque el widget permite elegirlos si se quiere)
    st.multiselect("Selecciona Reservas", options=reserves)
