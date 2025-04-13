import streamlit as st
import streamlit.components.v1 as components

# 1) Llamada a set_page_config al inicio
st.set_page_config(layout="wide")

# Indicador de versión para confirmar que se actualiza
st.write("### Versión 2.5 - Media Cancha Vertical (Revisado)")

# ------------------------------------------------
# 1. DATOS DE JUGADORES
# ------------------------------------------------
all_players = {
    "A": ["Axel"],  # Arquero
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

st.title("AS Montana - Squad")

# ------------------------------------------------
# 2. CONFIGURACIÓN DE LA FORMACIÓN
# ------------------------------------------------
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

# ------------------------------------------------
# 3. ASIGNACIÓN DE JUGADORES EN LA CANCHA (TITULARES)
# ------------------------------------------------
st.markdown("---")
st.header("Asignación de Jugadores en la Cancha")

def select_players(cat_key, num, key_prefix, label):
    """Permite asignar manualmente jugadores (sin repeticiones en la misma categoría)."""
    choices = []
    if num > 0:
        st.subheader(f"{label} (en cancha)")
        cols = st.columns(num)
        for i in range(num):
            # Cada selectbox solo muestra los que no se eligieron antes en la misma categoría
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

# ------------------------------------------------
# 4. SUPLENTES Y RESERVAS
# ------------------------------------------------
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

# ------------------------------------------------
# 5. VISUALIZACIÓN: MEDIA CANCHA VERTICAL
# ------------------------------------------------
# Estructura: 
#   - Ancho = 400
#   - Alto = 600
#   - y=0 es la línea de medio campo (arriba)
#   - y=600 es la línea de gol (abajo)
#   - Se dibuja el área penal y la portería al fondo
#   - Se coloca a los jugadores con top en %: 
#       Delanteros ~ 15%
#       Mediocampistas ~ 35%
#       Defensores ~ 55%
#       Arquero ~ 80% (para que quede sobre la portería)
# 
# Se incluye la línea horizontal en y=0 (medio campo)
# y=600 (gol), el rectángulo del área, la 6 yard box, punto penal y semicírculo.

col_field, col_lista = st.columns([3,2])  # Para que la lista quede más cerca
with col_field:
    st.header("AS MONTANA - SQUAD")

    # Formación real, e.g. "4-2-1"
    formation_str = f"{num_def}-{num_mid}-{num_fwd}"

    # Función para colocar jugadores
    def get_row_html(players, top_pct):
        html = ""
        valid = [p for p in players if p != "(Ninguno)"]
        if valid:
            n = len(valid)
            for i, player in enumerate(valid):
                left_pct = (i + 1) / (n + 1) * 100
                # Jugador = un círculo + nombre
                html += f"""
                <div style="position: absolute; top: {top_pct}%; left: {left_pct}%;
                            transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 24px; color: #fff;">●</div>
                    <div style="font-size: 16px; font-weight: bold; color: #fff;">{player}</div>
                </div>
                """
        return html

    # Jugadores en porcentajes verticales (arriba -> abajo)
    # Ajusta estos valores si los quieres más juntos o separados
    html_fwd = get_row_html(fwd_choices, 15)
    html_mid = get_row_html(mid_choices, 35)
    html_def = get_row_html(defender_choices, 55)
    html_gk  = get_row_html([arquero], 80)

    field_width = 400
    field_height = 600

    # Construimos la mitad de cancha (superior a inferior)
    #   y=0 es la línea media
    #   y=600 es la línea de gol
    # Dibujamos las líneas del arco y del área penal
    half_field_html = f"""
    <div style="position: relative; width: {field_width}px; height: {field_height}px;
                background-color: #1e7d36; border: 2px solid #000;">
        
        <!-- Línea central en y=0 -->
        <div style="position: absolute; left: 0px; top: 0px;
                    width: 100%; height: 2px; background: white;"></div>
                    
        <!-- Línea de gol en y=598 (abajo) -->
        <div style="position: absolute; left: 0px; top: 598px;
                    width: 100%; height: 2px; background: white;"></div>
        
        <!-- Arco: un rect pequeño centrado en x=200, y=600 ~ 610?? (opcional) -->
        <!-- Dibujo la portería (8 yardas ~ 80 px de ancho) centrada en x=200 -->
        <div style="
            position: absolute; left: 160px; top: 598px; 
            width: 80px; height: 8px; /* altura del marco del arco */
            border: 2px solid white;
            background: none;
            transform: translateY(0px);
        "></div>
        
        <!-- Área penal: 44 yardas ~ 132 px, definimos 120 px para simplificar -->
        <!-- Por ejemplo, x= (400-200)/2=100, ancho=200, 
             top=600-180=420, bottom=600 -->
        <div style="
            position: absolute; left: 100px; top: 420px; 
            width: 200px; height: 180px; 
            border: 2px solid #fff;
        "></div>

        <!-- Área chica: ~ 6 yard box. 
             x= (400-80)/2=160, ancho=80,
             top=600-60=540, bottom=600 -->
        <div style="
            position: absolute; left: 160px; top: 540px; 
            width: 80px; height: 60px; 
            border: 2px solid #fff;
        "></div>

        <!-- Punto penal: ~ 11 yards ~ 33 px desde la línea, 
             y=600 - 33=567, x=200 (centrado) -->
        <div style="
            position: absolute; left: 200px; top: 567px; 
            width: 5px; height: 5px; 
            background: #fff; 
            border-radius: 50%;
            transform: translate(-50%, -50%);
        "></div>

        <!-- Semicírculo (radio 60 px) centrado en x=200, y=567, 
             se muestra la parte superior del círculo -->
        <div style="
            position: absolute; left: 200px; top: 567px;
            width: 120px; height: 120px;
            margin-left: -60px; margin-top: -60px;
            border: 2px solid #fff;
            border-radius: 50%;
            background: none;
            clip-path: inset(60px 0 0 0); /* oculta la mitad inferior => semicírculo arriba */
        "></div>
        
        <!-- Jugadores en posiciones -->
        {html_fwd}
        {html_mid}
        {html_def}
        {html_gk}
    </div>
    """

    # Renderizamos
    components.html(half_field_html, height=field_height + 20)

    # Mostramos la formación
    st.markdown(f"**Formación elegida:** {formation_str}")

with col_lista:
    st.header("Suplentes (Fondo Oscuro)")
    supl_html = """
    <div style='background-color: #333; color: #fff; padding: 10px; border-radius: 5px;'>
    <h3 style='margin-top:0;'>Suplentes</h3>
    """
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
