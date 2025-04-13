import streamlit as st
import streamlit.components.v1 as components

# 1) Llamada temprana a set_page_config
st.set_page_config(layout="wide")

# Indicador de versión
st.write("### Versión 2.5 - Vertical Half Pitch")

# -------------------------------------------------
# 1. DATOS DE JUGADORES
# -------------------------------------------------
all_players = {
    "A": ["Axel"],  # Arquero
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

st.title("AS Montana - Squad")

# -------------------------------------------------
# 2. CONFIGURACIÓN DE LA FORMACIÓN
# -------------------------------------------------
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

# -------------------------------------------------
# 3. ASIGNACIÓN EN LA CANCHA (TITULARES)
# -------------------------------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

def select_players(cat_key, num, key_prefix, label):
    choices = []
    if num > 0:
        st.subheader(f"{label} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
            # Cada selectbox filtra jugadores ya elegidos en esa misma categoría
            available = ["(Ninguno)"] + [p for p in all_players[cat_key] if p not in choices]
            with cols[i]:
                sel = st.selectbox(f"{label} {i+1}", available, key=f"{key_prefix}_{i}")
            choices.append(sel)
    return choices

defender_choices = select_players("D", num_def, "def", "Defensores")
mid_choices      = select_players("M", num_mid, "mid", "Mediocampistas")
fwd_choices      = select_players("F", num_fwd, "fwd", "Delanteros")

arquero = all_players["A"][0]
dt = all_players["DT"][0]

st.markdown("#### Arquero")
st.write(f"**{arquero}**")
st.markdown("#### DT")
st.write(f"**{dt}**")

# -------------------------------------------------
# 4. SUPLENTES Y RESERVAS
# -------------------------------------------------
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

    used = set(defender_choices + mid_choices + fwd_choices + suplentes_def + suplentes_mid + suplentes_fwd)
    all_outfield = set(all_players["D"] + all_players["M"] + all_players["F"])
    reservas = sorted(list(all_outfield - used))

    st.markdown("---")
    st.subheader("Reservas")
    if reservas:
        for r in reservas:
            st.write("- " + r)
    else:
        st.write("Ninguna")

# -------------------------------------------------
# 5. VISUALIZACIÓN DE MEDIA CANCHA (VERTICAL) + SUPLENTES
# -------------------------------------------------
# La cancha será 400 px de ancho x 600 px de alto. Goal line abajo (y=600).
# Dibujamos las áreas, el arco, etc., y ubicamos a los jugadores en porcentaje vertical:
#   - 10% = cerca de la parte de arriba
#   - 30%/45% = intermedios
#   - 90% = abajo (arquero).
col_field, col_lista = st.columns([3, 2])
with col_field:
    st.header("AS MONTANA - SQUAD")

    # Cálculo de la formación en texto, ej. "2-3-1"
    formation_str = f"{num_def}-{num_mid}-{num_fwd}"

    # Función para posicionar los jugadores
    def get_row_html(players, top_pct):
        """
        players: lista de nombres (omitimos "(Ninguno)").
        top_pct: porcentaje vertical (0=arriba del todo, 100=abajo del todo).
        """
        html = ""
        valid = [p for p in players if p != "(Ninguno)"]
        if valid:
            n = len(valid)
            for i, player in enumerate(valid):
                left_pct = (i + 1) / (n + 1) * 100
                html += f"""
                <div style="position: absolute; 
                            top: {top_pct}%; 
                            left: {left_pct}%; 
                            transform: translate(-50%, -50%); 
                            text-align: center;">
                    <div style="font-size: 24px; color: #fff;">●</div>
                    <div style="font-size: 16px; font-weight: bold; color: #fff;">{player}</div>
                </div>
                """
        return html

    # Definimos las posiciones verticales: 
    #  - Delanteros al 15%
    #  - Mediocampistas al 35%
    #  - Defensores al 60%
    #  - Arquero al 85%
    html_fwd = get_row_html(fwd_choices, 15)
    html_mid = get_row_html(mid_choices, 35)
    html_def = get_row_html(defender_choices, 60)
    html_gk  = get_row_html([arquero], 85)

    field_width = 400
    field_height = 600

    # HTML de la media cancha
    #   - goal line horizontal en y=600
    #   - arco en y=600
    #   - rectángulos de área penal y área chica
    #   - punto penal y semicírculo
    html_half_field = f"""
    <div style="position: relative; width: {field_width}px; height: {field_height}px;
                background-color: #1e7d36; border: 2px solid #000; margin-bottom: 5px;">

        <!-- Goal line (horizontal) en la parte de abajo (y=598 approx) -->
        <div style="position: absolute; left: 0px; top: 598px; 
                    width: {field_width}px; height: 2px; background: white;"></div>

        <!-- Portería (arco). 
             Ancho ~60px, alto ~80px, centrado en x=200, parte inferior y=598. -->
        <div style="
            position: absolute; 
            left: 170px; top: 518px; 
            width: 60px; height: 80px;
            border: 2px solid #fff;
            background: none;">
        </div>

        <!-- Área penal (16.5 m) -> simulada ~110px de alto, 200px de ancho, centrada en x=200, 
             parte inferior en y=598. 
             top=598-110=488, left=100, width=200, height=110. -->
        <div style="
            position: absolute;
            left: 100px; top: 488px;
            width: 200px; height: 110px; 
            border: 2px solid #fff;">
        </div>

        <!-- Área chica (~55px de alto, 100px de ancho, centrada en x=200).
             top=598-55=543, left=150, width=100, height=55. -->
        <div style="
            position: absolute;
            left: 150px; top: 543px;
            width: 100px; height: 55px;
            border: 2px solid #fff;">
        </div>

        <!-- Punto penal:
             centrado en x=200, y ~ 598-77= 521 
             (entre la línea y el arco)
        -->
        <div style="
            position: absolute; 
            left: 200px; top: 521px;
            width: 4px; height: 4px;
            background: #fff;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        "></div>

        <!-- Semicírculo del penal:
             radio ~ 60px, centrado en (200, 521).
             Recuadro 120×120 con clip-path para mostrar sólo la mitad exterior. 
             top=521-60=461, left=200-60=140.
        -->
        <div style="
            position: absolute;
            left: 140px; top: 461px;
            width: 120px; height: 120px;
            border: 2px solid #fff;
            border-radius: 50%;
            background: none;
            clip-path: inset(0 60px 0 0);
        "></div>

        {html_fwd}
        {html_mid}
        {html_def}
        {html_gk}
    </div>
    """

    components.html(html_half_field, height=field_height + 20)

    # Mostrar la formación debajo de la cancha
    formation_text = f"**Formación elegida:** {formation_str}"
    st.markdown(formation_text)

with col_lista:
    st.header("Lista de Suplentes (Fondo Oscuro)")
    supl_html = "<div style='background-color: #333; color: #fff; padding: 10px; border-radius: 5px;'>"
    supl_html += "<h3 style='margin-top:0;'>Suplentes</h3>"
    if suplentes_def:
        supl_html += "<strong>Defensa:</strong><ul>" + "".join([f"<li>{p}</li>" for p in suplentes_def]) + "</ul>"
    else:
        supl_html += "<strong>Defensa:</strong> <em>Ninguno</em><br>"
    if suplentes_mid:
        supl_html += "<strong>Medio:</strong><ul>" + "".join([f"<li>{p}</li>" for p in suplentes_mid]) + "</ul>"
    else:
        supl_html += "<strong>Medio:</strong> <em>Ninguno</em><br>"
    if suplentes_fwd:
        supl_html += "<strong>Delanteros:</strong><ul>" + "".join([f"<li>{p}</li>" for p in suplentes_fwd]) + "</ul>"
    else:
        supl_html += "<strong>Delanteros:</strong> <em>Ninguno</em><br>"
    supl_html += "</div>"
    st.markdown(supl_html, unsafe_allow_html=True)
