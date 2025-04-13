import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(layout="wide")
st.write("### Versión 3.0 - Campo Vertical Corregido + Detalles Mejorados")

# ----------------------------------------
# 1. DATOS DE JUGADORES
# ----------------------------------------
all_players = {
    "A": ["Axel"],
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

st.title("AS Montana - Squad")

# ----------------------------------------
# 2. CONFIGURACIÓN DE LA FORMACIÓN
# ----------------------------------------
st.header("Configuración de la Formación")

total_players = st.number_input(
    "Número total de jugadores (incluyendo arquero)",
    min_value=1, max_value=11, value=6, step=1
)

num_field_players = total_players - 1

col_dist = st.columns(3)
with col_dist[0]:
    num_def = st.number_input("Defensores", min_value=0, max_value=num_field_players, value=2, step=1)
with col_dist[1]:
    num_mid = st.number_input("Mediocampistas", min_value=0, max_value=num_field_players, value=2, step=1)
with col_dist[2]:
    num_fwd = st.number_input("Delanteros", min_value=0, max_value=num_field_players, value=1, step=1)

if (num_def + num_mid + num_fwd) != num_field_players:
    st.error(f"La suma (Defensores + Mediocampistas + Delanteros) debe ser igual a {num_field_players}.")
    st.stop()

# Mostrar formación elegida tipo "2-3-2"
formation_str = f"{num_def}-{num_mid}-{num_fwd}"
st.markdown(f"**Formación elegida:** `{formation_str}`")

# ----------------------------------------
# 3. ASIGNACIÓN DE JUGADORES TITULARES
# ----------------------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

def select_players(cat_key, num, key_prefix, label):
    choices = []
    if num > 0:
        st.subheader(f"{label} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
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

# ----------------------------------------
# 4. SUPLENTES Y RESERVAS
# ----------------------------------------
st.markdown("---")
st.header("Suplentes y Reservas")

col_dummy, col_suplentes = st.columns([2,1])
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

# ----------------------------------------
# 5. VISUALIZACIÓN DE LA CANCHA (VERTICAL DE ABAJO HACIA ARRIBA)
# ----------------------------------------
col_field, col_lista = st.columns([3,2])
with col_field:
    st.header("AS MONTANA - SQUAD")

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

    # Invertimos las alturas para que el campo se vea desde abajo hacia arriba
    html_gk  = get_row_html([arquero], 85)
    html_def = get_row_html(defender_choices, 65)
    html_mid = get_row_html(mid_choices, 45)
    html_fwd = get_row_html(fwd_choices, 25)

    field_width = 400
    field_height = 600

    field_html = f"""
    <div style="position: relative; width: {field_width}px; height: {field_height}px;
                background-color: #1e7d36; border: 2px solid #000;">
        
        <!-- Línea de gol (abajo) -->
        <div style="position: absolute; left: 0px; top: 598px;
                    width: 100%; height: 2px; background: white;"></div>
                    
        <!-- Línea de medio campo (arriba) -->
        <div style="position: absolute; left: 0px; top: 0px;
                    width: 100%; height: 2px; background: white;"></div>
        
        <!-- Arco -->
        <div style="
            position: absolute; left: 160px; top: 598px; 
            width: 80px; height: 8px; 
            border: 2px solid white;
        "></div>

        <!-- Área penal -->
        <div style="
            position: absolute; left: 100px; top: 420px; 
            width: 200px; height: 180px; 
            border: 2px solid #fff;
        "></div>

        <!-- Área chica -->
        <div style="
            position: absolute; left: 160px; top: 540px; 
            width: 80px; height: 60px; 
            border: 2px solid #fff;
        "></div>

        <!-- Punto penal -->
        <div style="
            position: absolute; left: 200px; top: 567px; 
            width: 5px; height: 5px; 
            background: #fff; border-radius: 50%;
            transform: translate(-50%, -50%);
        "></div>

        <!-- Semicírculo -->
        <div style="
            position: absolute; left: 200px; top: 567px;
            width: 120px; height: 120px;
            margin-left: -60px; margin-top: -60px;
            border: 2px solid #fff;
            border-radius: 50%;
            background: none;
            clip-path: inset(60px 0 0 0);
        "></div>

        {html_fwd}
        {html_mid}
        {html_def}
        {html_gk}
    </div>
    """

    components.html(field_html, height=field_height + 20)

with col_lista:
    st.header("Suplentes")
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
