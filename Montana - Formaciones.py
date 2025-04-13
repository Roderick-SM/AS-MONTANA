import streamlit as st

# --- Datos de jugadores ---
all_players = {
    "A": ["Axel"],  # Arquero
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

# Configurar la página
st.set_page_config(layout="wide")
st.title("⚽ Organizador de Formaciones - Vista Cancha con Fondo")

# -------------------------------
# 1. CONFIGURACIÓN DE LA FORMACIÓN
# -------------------------------
st.header("Configuración de la Formación")

# Elegir número total de jugadores de campo (excluyendo arquero)
num_players = st.number_input(
    "Número de jugadores de campo (excluyendo arquero)",
    min_value=0, max_value=10, value=5, step=1
)

st.markdown("### Distribución de Jugadores en la Cancha")
col_dist = st.columns(3)
with col_dist[0]:
    num_def = st.number_input("Defensas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[1]:
    num_mid = st.number_input("Mediocampistas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[2]:
    num_fwd = st.number_input("Delanteros", min_value=0, max_value=num_players, value=1, step=1)

# Validar que la suma de posiciones coincida con el total
if (num_def + num_mid + num_fwd) != num_players:
    st.error("La suma de Defensas, Mediocampistas y Delanteros debe ser igual a " + str(num_players))
    st.stop()

# -------------------------------
# 2. ASIGNACIÓN MANUAL DE JUGADORES
# -------------------------------
st.markdown("---")
st.header("Asignación de Jugadores por Posición")
st.markdown("Selecciona el jugador para cada puesto. Si no asignás alguno, aparecerá como '(Ninguno)'.")

defender_choices = []
mid_choices = []
fwd_choices = []

# Asignar Defensas
if num_def > 0:
    st.subheader("Defensas")
    cols_def = st.columns(num_def)
    for i in range(num_def):
        with cols_def[i]:
            choice = st.selectbox(
                f"Defensa {i+1}",
                options=["(Ninguno)"] + all_players["D"],
                key=f"def_{i}"
            )
            defender_choices.append(choice)

# Asignar Mediocampistas
if num_mid > 0:
    st.subheader("Mediocampistas")
    cols_mid = st.columns(num_mid)
    for i in range(num_mid):
        with cols_mid[i]:
            choice = st.selectbox(
                f"Mediocampista {i+1}",
                options=["(Ninguno)"] + all_players["M"],
                key=f"mid_{i}"
            )
            mid_choices.append(choice)

# Asignar Delanteros
if num_fwd > 0:
    st.subheader("Delanteros")
    cols_fwd = st.columns(num_fwd)
    for i in range(num_fwd):
        with cols_fwd[i]:
            choice = st.selectbox(
                f"Delantero {i+1}",
                options=["(Ninguno)"] + all_players["F"],
                key=f"fwd_{i}"
            )
            fwd_choices.append(choice)

# Mostrar Arquero y DT fijos
st.markdown("#### Arquero")
arquero = all_players["A"][0]
st.markdown(f"**{arquero}**")

st.markdown("#### DT")
dt = all_players["DT"][0]
st.markdown(f"**{dt}**")

# -------------------------------
# 3. VISUALIZACIÓN EN LA CANCHA
# -------------------------------
st.markdown("---")
st.header("Visualización en la Cancha")

def get_row_html(players, top):
    """
    Genera HTML para una fila de jugadores en la cancha.
    :param players: Lista de nombres (se ignoran "(Ninguno)")
    :param top: Posición vertical en porcentaje (0 a 100)
    :return: HTML con divs posicionados absolutamente.
    """
    html = ""
    if players:
        N = len(players)
        for i, player in enumerate(players):
            left = (i + 1) / (N + 1) * 100  # Espaciado horizontal en porcentaje
            if player != "(Ninguno)":
                html += f'''
                <div style="position: absolute; top: {top}%; left: {left}%;
                            transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 24px;">●</div>
                    <div style="font-size: 14px;">{player}</div>
                </div>
                '''
    return html

# Definir posiciones verticales (en porcentaje) para cada línea;
# se han ajustado para acercarlas un poco más
top_forwards   = 25   # Delanteros
top_midfield   = 45   # Mediocampistas
top_defense    = 65   # Defensas
top_goalkeeper = 85   # Arquero

# Generar HTML para cada línea
html_forwards = get_row_html(fwd_choices, top_forwards)
html_midfield = get_row_html(mid_choices, top_midfield)
html_defense  = get_row_html(defender_choices, top_defense)
html_goalkeeper = f'''
<div style="position: absolute; top: {top_goalkeeper}%; left: 50%;
            transform: translate(-50%, -50%); text-align: center;">
    <div style="font-size: 24px;">●</div>
    <div style="font-size: 14px;">{arquero}</div>
</div>
'''

# Configuración de la cancha
field_width = 800
field_height = 600
# Fondo de cancha (una imagen de un terreno de fútbol)
field_bg = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Football_pitch.svg/800px-Football_pitch.svg.png"

# Combinar todo en un contenedor con fondo de la cancha
html_field = f'''
<div style="position: relative; width: {field_width}px; height: {field_height}px;
            background-image: url('{field_bg}'); background-size: cover; border: 2px solid #000;">
    {html_forwards}
    {html_midfield}
    {html_defense}
    {html_goalkeeper}
</div>
'''

st.markdown(html_field, unsafe_allow_html=True)
