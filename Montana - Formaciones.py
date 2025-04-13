import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.write("### Versión Final - Círculos por Posición + Suplentes Integrados + Fondo Gris")

# ------------------------------------------------
# 1) Datos de jugadores
# ------------------------------------------------
all_players = {
    "A": ["Axel", "Alex", "Gonza"],  # Arqueros
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],  # Defensores
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],  # Mediocampistas
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],  # Delanteros
    "DT": ["Diego"],
}

# Paleta de colores para cada posición
# Lo podés cambiar a gusto
category_colors = {
    "A": "#28a745",  # Verde para arquero
    "D": "#dc3545",  # Rojo para defensores
    "M": "#ffc107",  # Amarillo-anaranjado para mediocampistas
    "F": "#007bff",  # Azul para delanteros
}

def get_player_category(player):
    """Devuelve la categoría (A, D, M, F) para un jugador dado."""
    for cat in ["A", "D", "M", "F"]:
        if player in all_players[cat]:
            return cat
    return None

def get_player_color(player):
    """Devuelve el color de fondo para el jugador según su categoría."""
    cat = get_player_category(player)
    if cat and cat in category_colors:
        return category_colors[cat]
    return "#ffffff"  # blanco por si no encuentra la categoría

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
st.markdown(f"**Formación elegida:** `{formation_str}`")

# ------------------------------------------------
# 3) Selección de jugadores titulares
# ------------------------------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

arquero = st.selectbox("Elegí el arquero", all_players["A"])

def select_players(cat_key, num, key_prefix, label, exclude=[]):
    """Devuelve la lista de jugadores elegidos en esa categoría."""
    choices = []
    if num > 0:
        st.subheader(f"{label} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
            available = ["(Ninguno)"] + [
                p for p in all_players[cat_key]
                if p not in choices and p not in exclude
            ]
            with cols[i]:
                sel = st.selectbox(f"{label} {i+1}", available, key=f"{key_prefix}_{i}")
            choices.append(sel)
    return choices

# Excluir al arquero elegido de otras líneas
exclude_list = [arquero]
defender_choices = select_players("D", num_def, "def", "Defensores", exclude=exclude_list)
mid_choices = select_players("M", num_mid, "mid", "Mediocampistas", exclude=exclude_list)
fwd_choices = select_players("F", num_fwd, "fwd", "Delanteros", exclude=exclude_list)

# ------------------------------------------------
# 4) Suplentes y Reservas
# ------------------------------------------------
st.markdown("---")
st.header("Suplentes y Reservas")

suplentes_def = st.multiselect("Suplentes - Defensa:", options=[
    p for p in all_players["D"] if p not in defender_choices and p != arquero
])
suplentes_mid = st.multiselect("Suplentes - Medio:", options=[
    p for p in all_players["M"] if p not in mid_choices and p != arquero
])
suplentes_fwd = st.multiselect("Suplentes - Delanteros:", options=[
    p for p in all_players["F"] if p not in fwd_choices and p != arquero
])

used = set(
    defender_choices + mid_choices + fwd_choices +
    suplentes_def + suplentes_mid + suplentes_fwd + [arquero]
)
all_outfield = set(all_players["D"] + all_players["M"] + all_players["F"])
reservas = sorted(list(all_outfield - used))

st.markdown("---")
st.subheader("Reservas")
if reservas:
    for r in reservas:
        st.write("- " + r)
else:
    st.write("Ninguna")

# ------------------------------------------------
# 5) Construcción del "canvas" con cancha + suplentes
# ------------------------------------------------

def get_player_html(player, top_pct, left_pct):
    """ Devuelve el HTML de un jugador con círculo triple borde y color por posición. """
    if player == "(Ninguno)":
        return ""
    circle_color = get_player_color(player)
    # Círculo con triple borde: color base, anillo blanco, anillo negro
    # Se hace con: border: 2px solid #fff (borde blanco) + box-shadow: 0 0 0 2px #000 (borde negro)
    return f"""
    <div style="position: absolute; top: {top_pct}%; left: {left_pct}%;
                transform: translate(-50%, -50%); text-align: center;">
        <div style="
            width: 40px; height: 40px;
            border-radius: 50%;
            background: {circle_color};
            border: 2px solid #fff;
            box-shadow: 0 0 0 2px #000;
            margin: 0 auto;
        "></div>
        <div style="margin-top: 4px; font-size: 14px; color: #fff; font-weight: bold;">
            {player}
        </div>
    </div>
    """

def build_players_html(gk, defs, meds, fwds):
    """ Construye todo el HTML para los jugadores en sus posiciones (vertical). """
    result = ""
    # Arquero ~ 90%, Defs ~70%, Meds ~50%, Fwds ~30% (ajustable)
    # Distribución horizontal según cuántos jugadores haya en cada línea
    if gk:
        result += get_player_html(gk[0], 90, 50)  # 1 arquero centrado
    if defs:
        n = len(defs)
        for i, p in enumerate(defs):
            left_pct = (i + 1) / (n + 1) * 100
            result += get_player_html(p, 70, left_pct)
    if meds:
        n = len(meds)
        for i, p in enumerate(meds):
            left_pct = (i + 1) / (n + 1) * 100
            result += get_player_html(p, 50, left_pct)
    if fwds:
        n = len(fwds)
        for i, p in enumerate(fwds):
            left_pct = (i + 1) / (n + 1) * 100
            result += get_player_html(p, 30, left_pct)
    return result

players_html = build_players_html([arquero], defender_choices, mid_choices, fwd_choices)

# -------------------
# a) Cancha con "stripes" de fondo
# -------------------
# Podés cambiar '40px' o colores para otras franjas
field_html = f"""
<div style="position: absolute; left: 0; top: 0; width: 400px; height: 600px;
            background: repeating-linear-gradient(
                0deg,
                #1e7d36 0px,
                #1e7d36 40px,
                #24913c 40px,
                #24913c 80px
            );
            border-right: 2px solid #000; box-sizing: border-box;">

    <!-- Línea de medio campo -->
    <div style="position: absolute; top: 0px; left: 0; width: 100%; height: 2px; background: white;"></div>
    
    <!-- Punto central -->
    <div style="position: absolute; top: 0px; left: 200px;
                width: 6px; height: 6px;
                background: white; border-radius: 50%;
                transform: translate(-50%, 50%);"></div>
    
    <!-- Semicírculo central inferior -->
    <div style="
        position: absolute; top: -60px; left: 200px;
        width: 120px; height: 120px;
        margin-left: -60px;
        border: 2px solid #fff;
        border-radius: 50%;
        clip-path: inset(60px 0 0 0);
    "></div>
    
    <!-- Línea de gol -->
    <div style="position: absolute; top: 598px; left: 0; width: 100%; height: 2px; background: white;"></div>
    
    <!-- Arco -->
    <div style="position: absolute; left: 160px; top: 598px; width: 80px; height: 8px; border: 2px solid white;"></div>
    
    <!-- Área penal (más larga) -->
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
    
    {players_html}
</div>
"""

# -------------------
# b) Panel de suplentes (fondo gris)
# -------------------
suplentes_html = "<div style='position: absolute; right: 0; top: 0; width: 150px; height: 600px; "
suplentes_html += "background: #999; color: #fff; padding: 10px; box-sizing: border-box; font-size: 14px;'>"
suplentes_html += "<div style='text-align: center; font-weight: bold; margin-bottom: 10px;'>Suplentes</div>"

if suplentes_def:
    suplentes_html += "<div><strong>Defensa:</strong><ul style='margin:0; padding-left: 15px;'>"
    suplentes_html += "".join([f"<li style='list-style: disc; margin: 0;'>{p}</li>" for p in suplentes_def])
    suplentes_html += "</ul></div>"
else:
    suplentes_html += "<div><strong>Defensa:</strong> Ninguno</div>"

if suplentes_mid:
    suplentes_html += "<div><strong>Medio:</strong><ul style='margin:0; padding-left: 15px;'>"
    suplentes_html += "".join([f"<li style='list-style: disc; margin: 0;'>{p}</li>" for p in suplentes_mid])
    suplentes_html += "</ul></div>"
else:
    suplentes_html += "<div><strong>Medio:</strong> Ninguno</div>"

if suplentes_fwd:
    suplentes_html += "<div><strong>Delanteros:</strong><ul style='margin:0; padding-left: 15px;'>"
    suplentes_html += "".join([f"<li style='list-style: disc; margin: 0;'>{p}</li>" for p in suplentes_fwd])
    suplentes_html += "</ul></div>"
else:
    suplentes_html += "<div><strong>Delanteros:</strong> Ninguno</div>"

# DT
suplentes_html += f"<br><div><strong>DT:</strong> {all_players['DT'][0]}</div>"
suplentes_html += "</div>"

# -------------------
# c) Contenedor global (ancho: 400 + 150 = 550px)
# -------------------
overall_html = f"""
<div style="position: relative; width: 550px; height: 600px; border: 2px solid #000; margin-bottom: 20px;">
    {field_html}
    {suplentes_html}
</div>
"""

# Renderizamos todo como un solo bloque
st.subheader("Visualización Completa")
components.html(overall_html, height=620)
