import streamlit as st
import streamlit.components.v1 as components

# Configuración
st.set_page_config(layout="wide")
st.write("### Versión 3.4 - Círculo Central Corregido + Suplentes Más Cercanos")

# ---------------------------
# Datos de jugadores
# ---------------------------
all_players = {
    "A": ["Axel", "Alex", "Gonza"],
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

st.title("AS Montana - Squad")

# ---------------------------
# Configuración de formación
# ---------------------------
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

formation_str = f"{num_def}-{num_mid}-{num_fwd}"
st.markdown(f"**Formación elegida:** `{formation_str}`")

# ---------------------------
# Selección de titulares
# ---------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

arquero = st.selectbox("Elegí el arquero", all_players["A"])

def select_players(cat_key, num, key_prefix, label, exclude=[]):
    choices = []
    if num > 0:
        st.subheader(f"{label} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
            available = ["(Ninguno)"] + [p for p in all_players[cat_key] if p not in choices and p not in exclude]
            with cols[i]:
                sel = st.selectbox(f"{label} {i+1}", available, key=f"{key_prefix}_{i}")
            choices.append(sel)
    return choices

exclude_list = [arquero]

defender_choices = select_players("D", num_def, "def", "Defensores", exclude=exclude_list)
mid_choices = select_players("M", num_mid, "mid", "Mediocampistas", exclude=exclude_list)
fwd_choices = select_players("F", num_fwd, "fwd", "Delanteros", exclude=exclude_list)

# ---------------------------
# Suplentes y reservas
# ---------------------------
st.markdown("---")
st.header("Suplentes y Reservas")

col_dummy, col_suplentes = st.columns([1.9,1])
with col_suplentes:
    st.subheader("Suplentes")
    suplentes_def = st.multiselect("Defensa:", options=[p for p in all_players["D"] if p not in defender_choices and p != arquero])
    suplentes_mid = st.multiselect("Medio:", options=[p for p in all_players["M"] if p not in mid_choices and p != arquero])
    suplentes_fwd = st.multiselect("Delanteros:", options=[p for p in all_players["F"] if p not in fwd_choices and p != arquero])

    used = set(defender_choices + mid_choices + fwd_choices + suplentes_def + suplentes_mid + suplentes_fwd + [arquero])
    all_outfield = set(all_players["D"] + all_players["M"] + all_players["F"])
    reservas = sorted(list(all_outfield - used))

    st.markdown("---")
    st.subheader("Reservas")
    if reservas:
        for r in reservas:
            st.write("- " + r)
    else:
        st.write("Ninguna")

# ---------------------------
# Visualización de la cancha
# ---------------------------
col_field, col_lista = st.columns([4, 1])
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

    html_gk  = get_row_html([arquero], 90)
    html_def = get_row_html(defender_choices, 70)
    html_mid = get_row_html(mid_choices, 50)
    html_fwd = get_row_html(fwd_choices, 30)

    field_width = 400
    field_height = 600

    field_html = f"""
    <div style="position: relative; width: {field_width}px; height: {field_height}px;
                background-color: #1e7d36; border: 2px solid #000;">
        
        <!-- Línea de medio campo -->
        <div style="position: absolute; top: 0px; left: 0; width: 100%; height: 2px; background: white;"></div>
        
        <!-- Punto central -->
        <div style="position: absolute; top: 0px; left: 200px;
                    width: 6px; height: 6px;
                    background: white; border-radius: 50%;
                    transform: translate(-50%, 50%);"></div>


        <!-- Semicírculo central inferior (CORREGIDO) -->
        <div style="
            position: absolute; top: 50px; left: 200px;
            width: 120px; height: 120px;
            margin-left: -60px;
            border: 2px solid #fff;
            border-radius: 50%;
            clip-path: inset(60px 0 0 0);  /* muestra solo la mitad inferior */
        "></div>

        <!-- Línea de gol -->
        <div style="position: absolute; top: 598px; left: 0; width: 100%; height: 2px; background: white;"></div>

        <!-- Arco -->
        <div style="position: absolute; left: 160px; top: 598px; width: 80px; height: 8px; border: 2px solid white;"></div>

        <!-- Área penal más larga -->
        <div style="position: absolute; left: 60px; top: 460px; width: 280px; height: 140px; border: 2px solid white;"></div>

        <!-- Área chica -->
        <div style="position: absolute; left: 160px; top: 540px; width: 80px; height: 60px; border: 2px solid white;"></div>

        <!-- Semicírculo frente al área -->
        <div style="position: absolute; top: 460px; left: 200px;
                    width: 120px; height: 120px;
                    margin-left: -60px; margin-top: -60px;
                    border: 2px solid white;
                    border-radius: 50%;
                    clip-path: inset(0 0 60px 0);"></div>

        {html_fwd}
        {html_mid}
        {html_def}
        {html_gk}
    </div>
    """

    components.html(field_html, height=field_height + 20)

# ---------------------------
# Lista de suplentes con DT
# ---------------------------
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

    supl_html += f"<br><strong>DT:</strong> {all_players['DT'][0]}</div>"
    st.markdown(supl_html, unsafe_allow_html=True)
