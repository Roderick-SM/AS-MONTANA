import streamlit as st
import streamlit.components.v1 as components

# 1) Llamada temprana a set_page_config
st.set_page_config(layout="wide")

# Indicador de versión
st.write("### Versión 2.4 - Media Cancha + Área de Arqueros")

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
# 3. ASIGNACIÓN EN LA CANCHA (TITULARES)
# --------------------------
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

# --------------------------
# 4. SUPLENTES Y RESERVAS
# --------------------------
st.markdown("---")
st.header("Suplentes y Reservas")

# Selección de suplentes y cálculo de reservas
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

# --------------------------
# 5. VISUALIZACIÓN DE MEDIA CANCHA + SUPLENTES (AL LADO)
# --------------------------
# Para que estén más cerca, usamos columns([3,2]) en vez de [2,1]
col_field, col_lista = st.columns([3,2])
with col_field:
    st.header("AS MONTANA - SQUAD")

    # Función para posicionar jugadores horizontalmente,
    # con 'top' indicando la altura en % (del contenedor 600×400).
    def get_row_html(players, top_pct):
        html = ""
        valid = [p for p in players if p != "(Ninguno)"]
        if valid:
            n = len(valid)
            for i, player in enumerate(valid):
                left_pct = (i + 1) / (n + 1) * 100
                html += f"""
                <div style="position: absolute; top: {top_pct}%; left: {left_pct}%;
                            transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 24px; color: #fff;">●</div>
                    <div style="font-size: 16px; font-weight: bold; color: #fff;">{player}</div>
                </div>
                """
        return html

    # Cálculo de la formación, p. ej. "2-3-1"
    formation_str = f"{num_def}-{num_mid}-{num_fwd}"

    # Distancias verticales (de abajo hacia arriba):
    #  - Arquero: 85% (cerca del "fondo")
    #  - Defensores: 65%
    #  - Mediocampistas: 45%
    #  - Delanteros: 25%
    html_gk  = get_row_html([arquero], 85)
    html_def = get_row_html(defender_choices, 65)
    html_mid = get_row_html(mid_choices, 45)
    html_fwd = get_row_html(fwd_choices, 25)

    # Definimos contenedor "media cancha": 600×400
    # Dibujamos la portería, área penal, área chica, punto penal y un semicírculo.
    # La portería estará en x=0, la línea de media cancha en x=600 (no se dibuja, pues solo se ve "nuestra mitad").
    field_width = 600
    field_height = 400

    html_half_field = f"""
    <div style="position: relative; width: {field_width}px; height: {field_height}px;
                background-color: #1e7d36; border: 2px solid #000; margin-bottom: 5px;">

        <!-- Línea de gol (x=0) -->
        <div style="position: absolute; left: 0px; top: 0px; width: 2px; height: 100%; background: white;"></div>

        <!-- Portería: un rectángulo de 8% de ancho por 14% de alto (aprox) -->
        <div style="
            position: absolute; left: -10px; top: 160px; 
            width: 10px; height: 80px; 
            border: 2px solid #fff;
            background: none;
        "></div>

        <!-- Área penal: x=0..80, y=80..320 (rectángulo) -->
        <div style="
            position: absolute; left: 0px; top: 80px; 
            width: 80px; height: 240px; 
            border: 2px solid #fff;
        "></div>

        <!-- Área chica: x=0..35, y=140..260 (rectángulo) -->
        <div style="
            position: absolute; left: 0px; top: 140px; 
            width: 35px; height: 120px; 
            border: 2px solid #fff;
        "></div>

        <!-- Punto penal: x=60, y=200 (un punto blanco de 4x4px) -->
        <div style="
            position: absolute; left: 60px; top: 200px; 
            width: 4px; height: 4px; 
            background: #fff; 
            border-radius: 50%; 
            transform: translate(-50%, -50%);
        "></div>

        <!-- Semicírculo (radio=60px) centrado en x=60, y=200, mostrando la parte exterior:
             Para simplificar, dibujamos un círculo con overflow hidden para simular semicírculo.
        -->
        <div style="
            position: absolute; left: 60px; top: 200px; 
            width: 120px; height: 120px;
            margin-left: -60px; margin-top: -60px; 
            border: 2px solid #fff; 
            border-radius: 50%;
            background: none;
            clip-path: inset(0 0 0 60px); /* Muestra mitad derecha */
        "></div>

        <!-- {html_fwd} {html_mid} {html_def} {html_gk} -->
        {html_fwd}
        {html_mid}
        {html_def}
        {html_gk}
    </div>
    """

    # Renderizamos la media cancha
    components.html(html_half_field, height=field_height + 20)

    # Mostramos la formación debajo
    st.markdown(f"**Formación elegida:** {formation_str}")

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
