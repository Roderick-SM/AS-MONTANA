import streamlit as st

# --- Datos de jugadores ---
all_players = {
    "A": ["Axel"],  # Arquero
    "D": ["David", "Manu", "Joaco", "Sebastian", "Ale", "Gaston", "Marius", "Rodri A"],
    "M": ["Pedro", "Juan Colombia", "Alex", "Gonza", "Lauti", "Bash", "Nico", "Rodri P"],
    "F": ["Rodri SM", "Fer", "Parga", "Matheus", "Paco"],
    "DT": ["Diego"],
}

# Configuración de la página
st.set_page_config(layout="wide")
st.title("⚽ Organizador de Formaciones - Vista Cancha")

# --- CONFIGURACIÓN DE LA FORMACIÓN ---
st.header("Configuración de la Formación")

# 1) Elegir el número total de jugadores de campo (excluyendo arquero)
num_players = st.number_input(
    "Número de jugadores de campo (excluyendo arquero)",
    min_value=0, max_value=10, value=5, step=1
)

# 2) Definir cuántos serán Defensas, Mediocampistas y Delanteros
st.markdown("### Distribución de Jugadores en la Cancha")
col_dist = st.columns(3)
with col_dist[0]:
    num_def = st.number_input("Defensas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[1]:
    num_mid = st.number_input("Mediocampistas", min_value=0, max_value=num_players, value=2, step=1)
with col_dist[2]:
    num_fwd = st.number_input("Delanteros", min_value=0, max_value=num_players, value=1, step=1)

# Validación: La suma de D+M+F debe ser igual al total ingresado
if (num_def + num_mid + num_fwd) != num_players:
    st.error("La suma de Defensas, Mediocampistas y Delanteros debe ser igual a " + str(num_players))
    st.stop()

# --- ASIGNACIÓN MANUAL DE JUGADORES A POSICIONES ---
st.markdown("---")
st.header("Asignación de Jugadores por Posición")
st.markdown("Selecciona el jugador para cada puesto. Si aún no asignás alguno, aparecerá como '(Ninguno)'.")

# Listas para guardar la selección de cada línea
defender_choices = []
mid_choices = []
fwd_choices = []

# Sección de Defensas
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

# Sección de Mediocampistas
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

# Sección de Delanteros
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

# --- Visualización en la Cancha ---
st.markdown("---")
st.header("Visualización de la Formación (Estilo FIFA)")

def render_row(player_names):
    """
    Función para renderizar una fila (línea) de la cancha.
    Cada jugador se muestra con un puntito y su nombre centrado.
    """
    if player_names:
        num = len(player_names)
        row = st.columns(num)
        for idx, name in enumerate(player_names):
            with row[idx]:
                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<div style='font-size: 30px;'>●</div>"
                    f"<div>{name}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

# Visualizamos las líneas en orden inverso (los delanteros en la parte superior)
if fwd_choices:
    st.markdown("##### Delanteros")
    render_row(fwd_choices)

if mid_choices:
    st.markdown("##### Mediocampistas")
    render_row(mid_choices)

if defender_choices:
    st.markdown("##### Defensas")
    render_row(defender_choices)

# Mostrar el arquero fijo al fondo
st.markdown("##### Arquero")
st.markdown(
    f"<div style='text-align: center; font-size: 30px;'>"
    f"●<div>{all_players['A'][0]}</div></div>",
    unsafe_allow_html=True
)

# Mostrar DT (opcional) fuera del campo
st.markdown("---")
st.header("DT")
st.markdown(f"**{all_players['DT'][0]}**")
