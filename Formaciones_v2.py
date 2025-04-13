import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ------------------------------------------------
# 1) Datos de jugadores
# ------------------------------------------------
all_players = {
    "A": ["Axel", "Alex", "Gonza"],  # Arqueros
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A", "Alex"],  # Defensores
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],  # Mediocampistas
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],  # Delanteros
    "DT": ["Diego"],
}

# Colores según la opción 3:
category_colors = {
    "A": "#6f42c1",  # Púrpura para arquero
    "D": "#e83e8c",  # Rosa fuerte para defensores
    "M": "#fd7e8e",  # Naranja para mediocampistas  
    "F": "#20c997",  # Verde azulado para delanteros
}

# ------------------------------------------------
# 2) Configuración de la formación
# ------------------------------------------------
st.title("AS Montana - Squad")
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
st.markdown(f"**Formación elegida:** {formation_str}")

# --- SUBDIVISIÓN DE DEFENSORES (antes que mediocampistas) ---
st.markdown("### Subdivisión de Defensores")
col_def = st.columns(3)
num_def_central = col_def[0].number_input("Defensa Central", min_value=0, value=num_def, step=1)
num_def_izq = col_def[1].number_input("Lateral Izquierdo", min_value=0, value=0, step=1)
num_def_der = col_def[2].number_input("Lateral Derecho", min_value=0, value=0, step=1)
if num_def_central + num_def_izq + num_def_der != num_def:
    st.error("La suma de las subdivisiones de defensores debe ser igual al total de defensores.")
    st.stop()

# --- SUBDIVISIÓN DE MEDIOCAMPISTAS ---
st.markdown("### Subdivisión de Mediocampistas")
col_mid = st.columns(4)
num_mid_izq = col_mid[0].number_input("Medio Lateral Izquierdo", min_value=0, value=0, step=1)
num_mid_der = col_mid[1].number_input("Medio Lateral Derecho", min_value=0, value=0, step=1)
num_mid_def = col_mid[2].number_input("Medio Defensivo", min_value=0, value=num_mid, step=1)
num_mid_ofen = col_mid[3].number_input("Medio Ofensivo", min_value=0, value=0, step=1)
if num_mid_izq + num_mid_der + num_mid_def + num_mid_ofen != num_mid:
    st.error("La suma de las subdivisiones de mediocampistas debe ser igual a la cantidad total de mediocampistas.")
    st.stop()

# Scale is fixed at 1
scale = 1.0
field_width = int(400 * scale)
field_height = int(600 * scale)
suplentes_width = int(150 * scale)
overall_width = field_width + suplentes_width

# ------------------------------------------------
# 3) Selección de jugadores titulares
# ------------------------------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

# Selección del arquero
arquero = st.selectbox("Elegí el arquero", all_players["A"])

def select_players(category, num, key_prefix, label, exclude=[]):
    choices = []
    if num > 0:
        st.subheader(f"{label} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
            available = ["(Ninguno)"] + [p for p in all_players[category] if p not in choices and p not in exclude]
            with cols[i]:
                sel = st.selectbox(f"{label} {i+1}", available, key=f"{key_prefix}_{i}")
            choices.append(sel)
    return choices

exclude_list = [arquero]
def_central_choices = select_players("D", num_def_central, "defcent", "Defensa Central", exclude=exclude_list)
def_izq_choices    = select_players("D", num_def_izq,    "defizq",  "Lateral Izquierdo", exclude=exclude_list)
def_der_choices    = select_players("D", num_def_der,    "defder",  "Lateral Derecho", exclude=exclude_list)

mid_izq_choices  = select_players("M", num_mid_izq, "midizq", "Medio Lateral Izquierdo", exclude=exclude_list)
mid_der_choices  = select_players("M", num_mid_der, "midder", "Medio Lateral Derecho", exclude=exclude_list)
mid_def_choices  = select_players("M", num_mid_def, "middef", "Medio Defensivo", exclude=exclude_list)
mid_ofen_choices = select_players("M", num_mid_ofen, "midofen", "Medio Ofensivo", exclude=exclude_list)
fwd_choices      = select_players("F", num_fwd,     "fwd",    "Delanteros", exclude=exclude_list)

# ------------------------------------------------
# 4) Suplentes y Reservas (reservas eliminated)
# ------------------------------------------------
st.markdown("---")
st.header("Suplentes y Reservas")

suplentes_def = st.multiselect("Suplentes - Defensa:", 
    options=[p for p in all_players["D"] if p not in (def_central_choices + def_izq_choices + def_der_choices) and p != arquero])
suplentes_mid = st.multiselect("Suplentes - Medio:", 
    options=[p for p in all_players["M"] if p not in (mid_izq_choices + mid_der_choices + mid_def_choices + mid_ofen_choices) and p != arquero])
suplentes_fwd = st.multiselect("Suplentes - Delanteros:", 
    options=[p for p in all_players["F"] if p not in fwd_choices and p != arquero])

# ------------------------------------------------
# 5) Construcción del canvas con cancha y suplentes integrados
# ------------------------------------------------
# Function to generate HTML for a player
def get_player_html(player, top_pct, left_pct, cat):
    if player == "(Ninguno)":
        return ""
    return f"""
    <div style="position: absolute; top: {top_pct}%; left: {left_pct}%;
                transform: translate(-50%, -50%); text-align: center;">
        <div style="
            width: 40px; height: 40px;
            border-radius: 50%;
            background: {category_colors[cat]};
            border: 2px solid #fff;
            box-shadow: 0 0 0 2px #000;
            margin: 0 auto;
        "></div>
        <div style="margin-top: 4px; font-size: 14px; color: #fff; font-weight: bold;">
            {player}
        </div>
    </div>
    """

# Function to build HTML for subdivided defenders
def build_defenders_html(def_central, def_izq, def_der):
    result = ""
    if def_central:
        n = len(def_central)
        for i, p in enumerate(def_central):
            left_pct = (i + 1) / (n + 1) * 100
            result += get_player_html(p, 75, left_pct, "D")
    if def_izq:
        n = len(def_izq)
        for i, p in enumerate(def_izq):
            left_pct = 20 + (i - (n - 1) / 2) * 10
            result += get_player_html(p, 70, left_pct, "D")
    if def_der:
        n = len(def_der)
        for i, p in enumerate(def_der):
            left_pct = 80 + (i - (n - 1) / 2) * 10
            result += get_player_html(p, 70, left_pct, "D")
    return result

# Function to build HTML for a subgroup of midfielders
def build_subgroup_html(players, top_pct, center_x):
    html = ""
    if players:
        n = len(players)
        for i, player in enumerate(players):
            delta = (i - (n - 1) / 2) * 10  # Horizontal displacement
            left_pct = center_x + delta
            html += get_player_html(player, top_pct, left_pct, "M")
    return html

# Function to build the complete HTML for players on the field
def build_players_html(gk, def_cent, def_izq, def_der, mid_izq, mid_der, mid_def, mid_ofen, fwds):
    result = ""
    # Goalkeeper ~90% (category "A")
    if gk:
        result += get_player_html(gk[0], 90, field_width//2, "A")
    # Defenders subdivided:
    result += build_defenders_html(def_cent, def_izq, def_der)
    # Midfielders subdivided:
    result += build_subgroup_html(mid_izq, 50, 25)
    result += build_subgroup_html(mid_der, 50, 75)
    result += build_subgroup_html(mid_def, 60, 50)
    result += build_subgroup_html(mid_ofen, 40, 50)
    # Forwards ~25% (category "F")
    if fwds:
        n = len(fwds)
        for i, p in enumerate(fwds):
            left_pct = (i + 1) / (n + 1) * 100
            result += get_player_html(p, 25, left_pct, "F")
    return result

players_html = build_players_html(
    [arquero],
    def_central_choices,
    def_izq_choices,
    def_der_choices,
    mid_izq_choices,
    mid_der_choices,
    mid_def_choices,
    mid_ofen_choices,
    fwd_choices
)

# -------------------
# a) Field (left side, with fixed scale)
# -------------------
field_html = f"""
<div id="overall_container" style="position: absolute; left: 0; top: 0; width: {field_width}px; height: {field_height}px;
            background: repeating-linear-gradient(
                0deg,
                #1e7d36 0px,
                #1e7d36 {int(40*scale)}px,
                #24913c {int(40*scale)}px,
                #24913c {int(80*scale)}px
            );
            border-right: 2px solid #000; box-sizing: border-box;">
    
    <!-- Midline -->
    <div style="position: absolute; top: 0px; left: 0; width: 100%; height: 2px; background: white;"></div>
    
    <!-- Center point -->
    <div style="position: absolute; top: 0px; left: {field_width//2}px;
                width: 6px; height: 6px;
                background: white; border-radius: 50%;
                transform: translate(-50%, 50%);"></div>
    
    <!-- Bottom semicircle -->
    <div style="
        position: absolute; top: -{int(60*scale)}px; left: {field_width//2}px;
        width: {int(120*scale)}px; height: {int(120*scale)}px;
        margin-left: -{int(60*scale)}px;
        border: 2px solid #fff;
        border-radius: 50%;
        clip-path: inset({int(60*scale)}px 0 0 0);
    "></div>
    
    <!-- Goal line -->
    <div style="position: absolute; top: {field_height-2}px; left: 0; width: 100%; height: 2px; background: white;"></div>
    
    <!-- Goal -->
    <div style="position: absolute; left: {int(160*scale)}px; top: {field_height-2}px; width: {int(80*scale)}px; height: {int(8*scale)}px; border: 2px solid white;"></div>
    
    <!-- Penalty area -->
    <div style="position: absolute; left: {int(60*scale)}px; top: {int(500*scale)}px; width: {int(280*scale)}px; height: {int(120*scale)}px; border: 2px solid white;"></div>
    
    <!-- Small area -->
    <div style="position: absolute; left: {int(160*scale)}px; top: {int(580*scale)}px; width: {int(80*scale)}px; height: {int(60*scale)}px; border: 2px solid white;"></div>
    
    <!-- Front semicircle -->
    <div style="position: absolute; top: {int(500*scale)}px; left: {field_width//2}px;
                width: {int(120*scale)}px; height: {int(120*scale)}px;
                margin-left: -{int(60*scale)}px; margin-top: -{int(60*scale)}px;
                border: 2px solid white;
                border-radius: 50%;
                clip-path: inset(0 0 {int(60*scale)}px 0);
    "></div>
    
    {players_html}
</div>
"""

# -------------------
# b) Suplentes panel (right side, fixed scale)
# -------------------
suplentes_html = f"<div style='position: absolute; right: 0; top: 0; width: {suplentes_width}px; height: {field_height}px; background: #999; color: #fff; padding: 10px; box-sizing: border-box; font-size: 18px;'>"
suplentes_html += "<div style='text-align: center; font-weight: bold; margin-bottom: 20px;'>Suplentes</div>"

if suplentes_fwd:
    suplentes_html += "<div style='margin-bottom: 15px;'><strong>Delanteros:</strong><ul style='margin:0; padding-left: 15px;'>" + "".join([f"<li style='list-style: disc; margin: 0 0 5px 0;'>{p}</li>" for p in suplentes_fwd]) + "</ul></div>"
else:
    suplentes_html += "<div style='margin-bottom: 15px;'><strong>Delanteros:</strong> Ninguno</div>"

if suplentes_mid:
    suplentes_html += "<div style='margin-bottom: 15px;'><strong>Medio:</strong><ul style='margin:0; padding-left: 15px;'>" + "".join([f"<li style='list-style: disc; margin: 0 0 5px 0;'>{p}</li>" for p in suplentes_mid]) + "</ul></div>"
else:
    suplentes_html += "<div style='margin-bottom: 15px;'><strong>Medio:</strong> Ninguno</div>"

if suplentes_def:
    suplentes_html += "<div style='margin-bottom: 15px;'><strong>Defensa:</strong><ul style='margin:0; padding-left: 15px;'>" + "".join([f"<li style='list-style: disc; margin: 0 0 5px 0;'>{p}</li>" for p in suplentes_def]) + "</ul></div>"
else:
    suplentes_html += "<div style='margin-bottom: 15px;'><strong>Defensa:</strong> Ninguno</div>"

suplentes_html += "<div style='margin-top: 20px; text-align: center;'><strong>DT:</strong> " + all_players['DT'][0] + "</div>"
suplentes_html += "<div style='margin-top: 20px; text-align: center; font-size: 22px; font-weight: bold;'><strong>Formacion:</strong> <span style='font-size: 22px; font-weight: bold;'>" + formation_str + "</span></div>"
suplentes_html += "</div>"

# -------------------
# c) Global container (100% width with max-width)
# -------------------
overall_html = r"""
<div id="overall_container" style="position: relative; width: 100%; max-width: """ + f"{overall_width}px; height: {field_height}px; border: 2px solid #000; margin: auto; margin-bottom: 20px;">" + r"""
    """ + field_html + r"""
    """ + suplentes_html + r"""
</div>
<div style="text-align: center; margin-bottom: 20px;">
  <button onclick="downloadImage()" style="padding: 10px; font-size: 16px;">Descargar Imagen</button>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function downloadImage() {
    html2canvas(document.getElementById("overall_container")).then(function(canvas) {
        var link = document.createElement('a');
        link.download = 'squad.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}
</script>
"""

st.subheader("AS MONTANA - Squad")
components.html(overall_html, height=field_height+100)
