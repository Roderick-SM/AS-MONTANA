import streamlit as st
import streamlit.components.v1 as components

# --- DATOS DE JUGADORES ---
all_players = {
    "A": ["Axel"],  # Arquero
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

st.set_page_config(layout="wide")
st.title("AS Montana - Squad")

# -------------------------------------------------
# 1) CONFIGURACIÓN DE LA FORMACIÓN
# -------------------------------------------------
st.header("Configuración de la Formación")

num_players = st.number_input(
    "Número de jugadores de campo (excluyendo arquero)",
    min_value=0, max_value=10, value=5, step=1
)

col_dist = st.columns(3)
with col_dist[0]:
    num_def = st.number_input("Defensas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[1]:
    num_mid = st.number_input("Mediocampistas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[2]:
    num_fwd = st.number_input("Delanteros", min_value=0, max_value=num_players, value=1, step=1)

if (num_def + num_mid + num_fwd) != num_players:
    st.error(f"La suma (Defensas + Mediocampistas + Delanteros) debe ser igual a {num_players}. Corrígelo antes de continuar.")
    st.stop()

# -------------------------------------------------
# 2) ASIGNACIÓN MANUAL DE JUGADORES A CADA POSICIÓN
# -------------------------------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

# Para evitar repeticiones, cada selectbox se alimenta de los nombres aún no usados en esa categoría.
# Nota: Se recorren las posiciones de forma secuencial para que cada elección vaya filtrando las siguientes.
def select_players(category, num, key_prefix):
    choices = []
    if num > 0:
        cols = st.columns(num)
        st.subheader(f"{category}s")
        for i in range(num):
            # Opciones: "(Ninguno)" + los nombres que aún no fueron elegidos en esta categoría.
            available = ["(Ninguno)"] + [p for p in all_players[category] if p not in choices]
            with cols[i]:
                sel = st.selectbox(f"{category} {i+1}", available, key=f"{key_prefix}_{i}")
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

# -------------------------------------------------
# 3) VISUALIZACIÓN DE LA CANCHA (FORMACIÓN) EN ORIENTACIÓN HORIZONTAL
# -------------------------------------------------
st.markdown("---")
st.header("Visualización en la Cancha")

# Para una cancha horizontal al estilo fútbol (como en muchos diagramas de formación),
# se distribuyen los jugadores en columnas:
#   - GK: Columna fija en el extremo (izquierda)
#   - Defensas: Columna a la derecha del GK (p.ej., x = 250)
#   - Mediocampistas: En columna central (x = 450)
#   - Delanteros: En columna derecha (x = 650)
#
# La función get_column_html dispone a los jugadores verticalmente en la columna dada.
def get_column_html(players, left):
    html = ""
    valid = [p for p in players if p != "(Ninguno)"]
    if valid:
        n = len(valid)
        for i, player in enumerate(valid):
            # Distribuir verticalmente: usamos porcentaje del alto del contenedor.
            y = (i + 1) / (n + 1) * 100  # en %
            html += f"""
            <div style="position: absolute; left: {left}px; top: {y}%;
                        transform: translate(-50%, -50%); text-align: center;">
                <div style="font-size: 36px; line-height: 32px; color: #fff;">●</div>
                <div style="font-size: 20px; font-weight: bold; color: #fff;">{player}</div>
            </div>
            """
    return html

# Definir posiciones horizontales (en px) para cada grupo
x_gk = 50      # Arquero
x_def = 250    # Defensas
x_mid = 450    # Mediocampistas
x_fwd = 650    # Delanteros

html_gk  = get_column_html([arquero], x_gk)
html_def = get_column_html(defender_choices, x_def)
html_mid = get_column_html(mid_choices, x_mid)
html_fwd = get_column_html(fwd_choices, x_fwd)

# La cancha: contenedor de 800x550 px en fondo verde uniforme, con líneas de campo (línea central vertical y círculo central).
field_width = 800
field_height = 550

html_field = f"""
<div style="position: relative; width: {field_width}px; height: {field_height}px;
         background-color: #1e7d36; border: 2px solid #000; margin-bottom: 20px;">
    <!-- Línea central vertical -->
    <div style="position: absolute; left: {field_width/2}px; top: 0; width: 2px; height: 100%; background: white;"></div>
    <!-- Círculo central -->
    <div style="position: absolute; left: {field_width/2}px; top: 50%; width: 80px; height: 80px;
         margin-left: -40px; margin-top: -40px; border: 2px solid white; border-radius: 50%;"></div>
    {html_gk}
    {html_def}
    {html_mid}
    {html_fwd}
</div>
"""

components.html(html_field, height=field_height + 40)

# -------------------------------------------------
# 4) SECCIÓN DE SUPLENTES Y RESERVAS (Columna derecha)
# -------------------------------------------------
st.markdown("---")
st.header("Suplentes y Reservas")

# Disponer la visualización en dos columnas: 
# la cancha (ya en la parte izquierda arriba) y a la derecha los widgets para suplentes y reservas.
col_dummy, col_banco = st.columns([2, 1])  # La columna de la derecha más estrecha

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
    # Calculamos los jugadores del outfield (D, M, F) que NO están asignados ni en la cancha ni en suplentes.
    used_field = set(defender_choices + mid_choices + fwd_choices + bench_def + bench_mid + bench_fwd)
    all_outfield = set(all_players["D"] + all_players["M"] + all_players["F"])
    available_reserves = sorted(list(all_outfield - used_field))
    reservas = st.multiselect("Selecciona Reservas", options=available_reserves)
