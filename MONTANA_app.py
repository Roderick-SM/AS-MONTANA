import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Datos iniciales en categorías iniciales
def init_data():
    return {
        "Disponible": ['Axel', 'Rodri SM', 'Fer', 'Pedro', 'David', 'Manu', 'Parga', 'Juan Colombia', 'Alex', 'Matheus'],
        "No puede": ['Joaco'],
        "No responde": ['Gonza', 'Lauti', 'Bash', 'Paco', 'Sebastian'],
        "Fuera de París": ['Ale', 'Nico', 'Rodri P', 'Gaston', 'Marius'],
        "Lesionado": ['Rodri A'],
        "No Juega": ['Diego']
    }

# Inicialización
if 'jugadores' not in st.session_state:
    st.session_state.jugadores = init_data()

# Interfaz para mover jugadores
st.title("AS MONTANA - Gestión jugadores")

# Mover jugador
with st.sidebar:
    st.header("Mover jugador entre categorías")
    jugador = st.selectbox("Selecciona jugador", sum(st.session_state.jugadores.values(), []))
    nueva_categoria = st.selectbox("Nueva categoría", list(st.session_state.jugadores.keys()))

    if st.button("Mover jugador"):
        # Remover de categoría anterior
        for cat in st.session_state.jugadores:
            if jugador in st.session_state.jugadores[cat]:
                st.session_state.jugadores[cat].remove(jugador)
                break
        # Añadir a nueva categoría
        st.session_state.jugadores[nueva_categoria].append(jugador)

# Dibujar cancha y jugadores
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 100)
ax.set_ylim(0, 50)

# Fondo
ax.add_patch(patches.Rectangle((0, 0), 50, 50, color='#7FCB7F'))
ax.add_patch(patches.Rectangle((50, 0), 50, 50, color='#B1D7A3'))
ax.plot([50, 50], [0, 50], color="white", linewidth=2)
ax.add_patch(patches.Circle((50, 25), 7, edgecolor='white', facecolor='none', linewidth=2))

# Títulos
ax.text(20, 47, "DISPONIBLES", fontsize=16, weight='bold', color='darkgreen', ha='center')
ax.text(75, 47, "NO DISPONIBLES", fontsize=16, weight='bold', color='darkred', ha='center')

# Función posiciones
def generate_positions(x, n, top=43, bottom=13):
    if n == 1:
        return [(x, (top + bottom) / 2)]
    spacing = (top - bottom) / (n - 1)
    return [(x, top - i * spacing) for i in range(n)]

# Graficar jugadores
colores = {'Disponible': '#1E90FF', 'No responde': '#FF8C00', 'Fuera de París': '#FFD700', 
           'No puede': '#808080', 'Lesionado': '#FF6347', 'No Juega': '#000000'}

# Posiciones específicas según categoría
x_posiciones = {'Disponible': 20, 'No responde': 63, 'Fuera de París': 73, 'No puede': 83, 'Lesionado': 83, 'No Juega': 93}
y_limites = {'Disponible': (43,13), 'No responde': (43,10), 'Fuera de París': (40,15), 'No puede': (45,30), 'Lesionado': (27,10)}

for cat, jugadores in st.session_state.jugadores.items():
    if cat != 'No Juega':
        top, bottom = y_limites[cat]
        pos = generate_positions(x_posiciones[cat], len(jugadores), top, bottom)
        for p, name in zip(pos, jugadores):
            ax.plot(p[0], p[1], 'o', markersize=15, color=colores[cat])
            ax.text(p[0], p[1]-2, name, ha='center', fontsize=10, weight='bold')
    else:
        ax.plot(x_posiciones[cat], 25, 'o', markersize=15, color=colores[cat])
        ax.text(x_posiciones[cat], 21, jugadores[0], ha='center', fontsize=10, weight='bold')

# Totales
ax.text(20, 2, f"TOTAL: {len(st.session_state.jugadores['Disponible'])}", fontsize=14, weight='bold', ha='center')
total_no_disponible = sum(len(st.session_state.jugadores[cat]) for cat in st.session_state.jugadores if cat != 'Disponible')
ax.text(75, 2, f"TOTAL: {total_no_disponible}", fontsize=14, weight='bold', ha='center')

# Leyenda en una sola fila
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), fontsize=12, ncol=6)
ax.axis('off')
st.pyplot(fig)
