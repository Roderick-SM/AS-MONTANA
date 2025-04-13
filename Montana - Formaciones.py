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
st.title("⚽ Organizador de Formaciones - Cancha Verde + Suplentes + DT")

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
    st.error(f"La suma (D+M+F) debe ser igual a {num_players}. Corrígelo antes de continuar.")
    st.stop()

# -------------------------------------------------
# 2) ASIGNACIÓN MANUAL DE JUGADORES
# -------------------------------------------------
st.markdown("---")
st.header("Asignación de Jugadores por Posición")
st.markdown("Selecciona el jugador para cada puesto. Si no asignás alguno, aparecerá '(Ninguno)'.")

defender_choices = []
mid_choices = []
fwd_choices = []

# Defensas
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

# Mediocampistas
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

# Delanteros
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

# Arquero y DT (fijos)
st.markdown("#### Arquero")
arquero = all_players["A"][0]
st.write(f"**{arquero}**")

st.markdown("#### DT")
dt = all_players["DT"][0]
st.write(f"**{dt}**")

# -------------------------------------------------
# 3) VISUALIZACIÓN EN LA CANCHA (columna izquierda)
#    + SUPLENTES Y DT EN LA DERECHA
# -------------------------------------------------
st.markdown("---")
st.header("Vista en Cancha + Suplentes")

# Creamos dos columnas: cancha (3 partes) y banco (1 parte)
col_cancha, col_banco = st.columns([3, 1])

#
# A) CANCHA
#
with col_cancha:
    def get_row_html(players, top):
        """
        Genera HTML para una fila de jugadores en la cancha.
        :param players: Lista de nombres (ignoramos "(Ninguno)")
        :param top: Posición vertical en porcentaje (0 a 100)
        :return: HTML con divs posicionados absolutamente.
        """
        html = ""
        if players:
            valid_players = [p for p in players if p != "(Ninguno)"]
            N = len(valid_players)
            for i, player in enumerate(valid_players):
                # Distribuimos horizontalmente en porcentaje
                left = (i + 1) / (N + 1) * 100  
                html += f'''
                <div style="position: absolute; top: {top}%; left: {left}%;
                            transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 36px; line-height: 32px;">●</div>
                    <div style="font-size: 20px; font-weight: bold;">{player}</div>
                </div>
                '''
        return html

    # Ajustamos porcentajes de cada línea
    top_forwards   = 25   # Delanteros
    top_midfield   = 50   # Mediocampistas
    top_defense    = 75   # Defensas
    top_goalkeeper = 90   # Arquero

    # Generamos HTML para cada línea
    html_forwards = get_row_html(fwd_choices, top_forwards)
    html_midfield = get_row_html(mid_choices, top_midfield)
    html_defense  = get_row_html(defender_choices, top_defense)
    html_goalkeeper = f"""
    <div style="position: absolute; top: {top_goalkeeper}%; left: 50%;
                transform: translate(-50%, -50%); text-align: center;">
        <div style="font-size: 36px; line-height: 32px;">●</div>
        <div style="font-size: 20px; font-weight: bold;">{arquero}</div>
    </div>
    """

    # Imagen de la cancha verde con líneas
    field_width = 800
    field_height = 550
    field_bg = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Football_pitch.svg/1200px-Football_pitch.svg.png"

    # Contenedor HTML con la cancha de fondo
    html_field = f"""
    <div style="position: relative; width: {field_width}px; height: {field_height}px;
                background: url('{field_bg}') no-repeat center/cover;
                border: 2px solid #000; margin-bottom: 20px;">
        {html_forwards}
        {html_midfield}
        {html_defense}
        {html_goalkeeper}
    </div>
    """

    # Renderizamos el HTML
    components.html(html_field, height=field_height + 40)

#
# B) BANCO DE SUPLENTES + DT
#
with col_banco:
    st.subheader("Suplentes")

    # Para listar suplentes, calculamos quién NO fue elegido en cada posición
    chosen_defenders = [p for p in defender_choices if p != "(Ninguno)"]
    chosen_mids      = [p for p in mid_choices if p != "(Ninguno)"]
    chosen_forwards  = [p for p in fwd_choices if p != "(Ninguno)"]

    bench_def = sorted(set(all_players["D"]) - set(chosen_defenders))
    bench_mid = sorted(set(all_players["M"]) - set(chosen_mids))
    bench_fwd = sorted(set(all_players["F"]) - set(chosen_forwards))

    # Mostramos suplentes por posición (solo si hay alguno)
    if bench_def:
        st.markdown("**Defensas**")
        for p in bench_def:
            st.write(p)

    if bench_mid:
        st.markdown("**Mediocampistas**")
        for p in bench_mid:
            st.write(p)

    if bench_fwd:
        st.markdown("**Delanteros**")
        for p in bench_fwd:
            st.write(p)

    # Al final, DT
    st.markdown("---")
    st.subheader("DT")
    st.write(dt)
