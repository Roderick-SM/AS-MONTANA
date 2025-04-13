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

col_dist = st.columns(3)
with col_dist[0]:
    num_def = st.number_input("Defensores", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[1]:
    num_mid = st.number_input("Mediocampistas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[2]:
    num_fwd = st.number_input("Delanteros", min_value=0, max_value=num_players, value=1, step=1)

if (num_def + num_mid + num_fwd) != num_players:
    st.error(f"La suma (Defensores + Mediocampistas + Delanteros) debe ser igual a {num_players}.")
    st.stop()

# --------------------------
# 3. ASIGNACIÓN DE JUGADORES EN LA CANCHA
# --------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

def select_players(cat_key, num, key_prefix, label):
    choices = []
    if num > 0:
        st.subheader(f"{label} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
            # Evitamos repetir: cada select box muestra solo los nombres aún no elegidos en esa categoría.
            available = ["(Ninguno)"] + [p for p in all_players[cat_key] if p not in choices]
            with cols[i]:
                sel = st.selectbox(f"{label} {i+1}", available, key=f"{key_prefix}_{i}")
            choices.append(sel)
    return choices

# Títulos completos para cada sección
defender_choices = select_players("D", num_def, "def", "Defensores")
mid_choices      = select_players("M", num_mid, "mid", "Mediocampistas")
fwd_choices      = select_players("F", num_fwd, "fwd", "Delanteros")

arquero = all_players["A"][0]
dt = all_players["DT"][0]

st.markdown("#### Arquero")
st.write(f"**{arquero}**")
st.markdown("#### DT")
st.write(f"**{dt}**")

# --------------------------
# 4. SUPLENTES Y RESERVAS
# --------------------------
# Esta sección se procesa antes de visualizar la cancha,
# de modo que se considere la selección de suplentes y se calculen las reservas.
st.markdown("---")
st.header("Suplentes y Reservas")

col_dummy, col_suplentes = st.columns([2, 1])
with col_suplentes:
    st.subheader("Suplentes")
    suplentes_def = st.multiselect(
        "Defensa:", options=[p for p in all_players["D"] if p not in defender_choices]
    )
    suplentes_mid = st.multiselect(
        "Medio:", options=[p for p in all_players["M"] if p not in mid_choices]
    )
    suplentes_fwd = st.multiselect(
        "Delanteros:", options=[p for p in all_players["F"] if p not in fwd_choices]
    )
    st.markdown("**DT:**")
    st.write(dt)
    usados = set(defender_choices + mid_choices + fwd_choices + suplentes_def + suplentes_mid + suplentes_fwd)
    all_outfield = set(all_players["D"] + all_players["M"] + all_players["F"])
    reservas = sorted(list(all_outfield - usados))
    st.markdown("---")
    st.subheader("Reservas")
    if reservas:
        st.markdown("\n".join([f"- {p}" for p in reservas]))
    else:
        st.markdown("Ninguna")

# --------------------------
# 5. VISUALIZACIÓN DE LA CANCHA (ORIENTACIÓN VERTICAL)
# --------------------------
# Aquí se muestra la visualización después de elegir suplentes, en una sección separada.
# La cancha se define con un contenedor vertical (ancho 550px, alto 800px).
col_field, col_dummy2 = st.columns([2, 1])
with col_field:
    st.header("AS MONTANA - SQUAD")  # Título de la visualización
    def get_row_html(players, top_pct):
        """Genera HTML para una fila de jugadores, distribuidos horizontalmente."""
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

    # Asignamos los porcentajes verticales para una cancha que es vertical:
    # De abajo hacia arriba: Arquero (base), Defensores, Mediocampistas, Delanteros (cima)
    html_arquero = get_row_html([arquero], 90)
    html_def     = get_row_html(defender_choices, 70)
    html_mid     = get_row_html(mid_choices, 45)
    html_fwd     = get_row_html(fwd_choices, 20)
    
    # Definimos la cancha vertical: ancho menor y alto mayor.
    field_width = 550
    field_height = 800

    html_field = f"""
    <div style="position: relative; width: {field_width}px; height: {field_height}px;
             background-color: #1e7d36; border: 2px solid #000; margin-bottom: 20px;">
        <!-- Línea central horizontal -->
        <div style="position: absolute; top: {field_height/2}px; left: 0;
                    width: 100%; height: 2px; background: white;"></div>
        <!-- Círculo central -->
        <div style="position: absolute; left: 50%; top: 50%; width: 80px; height: 80px;
                    margin-left: -40px; margin-top: -40px; border: 2px solid white; border-radius: 50%;"></div>
        {html_fwd}
        {html_mid}
        {html_def}
        {html_arquero}
    </div>
    """

    components.html(html_field, height=field_height + 40)

    # Mostrar, a la derecha del contenedor (en la misma columna si es posible), la lista de suplentes
    st.subheader("Suplentes (en lista)")
    if suplentes_def:
        st.markdown("**Defensa:**")
        st.markdown("\n".join([f"- {p}" for p in suplentes_def]))
    if suplentes_mid:
        st.markdown("**Medio:**")
        st.markdown("\n".join([f"- {p}" for p in suplentes_mid]))
    if suplentes_fwd:
        st.markdown("**Delanteros:**")
        st.markdown("\n".join([f"- {p}" for p in suplentes_fwd]))
