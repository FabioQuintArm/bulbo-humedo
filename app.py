import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

st.set_page_config(page_title="Simulador de Bulbo Húmedo", layout="centered")

st.title("💧 Simulador de Bulbo Húmedo en Riego por Goteo")

st.markdown("Introduce los datos del suelo y del riego para estimar el perfil húmedo generado por un gotero.")

# Entradas del usuario
with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        arena = st.number_input("Arena (%)", min_value=0, max_value=100, value=50)
    with col2:
        limo = st.number_input("Limo (%)", min_value=0, max_value=100, value=30)
    with col3:
        arcilla = st.number_input("Arcilla (%)", min_value=0, max_value=100, value=20)

    if arena + limo + arcilla != 100:
        st.warning("⚠️ La suma de los porcentajes debe ser 100%.")
        calcular = False
    else:
        calcular = True

    caudal = st.number_input("Caudal del gotero (L/h)", min_value=0.1, step=0.1, value=4.0)
    tiempo = st.number_input("Tiempo de riego (minutos)", min_value=1, step=1, value=30)

    submitted = st.form_submit_button("Calcular bulbo")

# Clasificación USDA simplificada
def clasificar_textura(arena, limo, arcilla):
    if arcilla >= 40:
        return "Arcilla"
    elif arcilla >= 27 and limo >= 28:
        return "Arcilla limosa"
    elif arcilla >= 27:
        return "Franco arcilloso"
    elif limo >= 40 and arcilla < 20:
        return "Franco limoso"
    elif arena >= 70 and limo < 15 and arcilla < 15:
        return "Arena"
    elif arena >= 52 and limo < 28 and arcilla < 20:
        return "Franco arenoso"
    elif limo >= 28 and arcilla >= 7 and arcilla < 27:
        return "Franco"
    else:
        return "Franco"

# Tabla de coeficientes Ka y Kp
coeficientes = {
    "Arena": (0.75, 1.10),
    "Franco arenoso": (0.70, 1.20),
    "Franco": (0.65, 1.30),
    "Franco limoso": (0.60, 1.35),
    "Franco arcilloso": (0.55, 1.45),
    "Arcilla limosa": (0.50, 1.50),
    "Arcilla": (0.45, 1.55)
}

# Cálculo y visualización
if submitted and calcular:
    textura = clasificar_textura(arena, limo, arcilla)
    Ka, Kp = coeficientes.get(textura, (0.60, 1.35))  # valores por defecto

    t_horas = tiempo / 60
    volumen = caudal * t_horas

    A = Ka * np.sqrt(volumen)
    P = Kp * np.sqrt(volumen)

    st.subheader("🧪 Resultados")
    st.write(f"**Textura estimada:** {textura}")
    st.write(f"**Ka:** {Ka}  |  **Kp:** {Kp}")
    st.write(f"**Ancho estimado del bulbo:** {A:.1f} cm")
    st.write(f"**Profundidad estimada del bulbo:** {P:.1f} cm")

    # Gráfico del perfil (elipse)
    fig, ax = plt.subplots(figsize=(4, 6))
    bulbo = Ellipse(xy=(0, -P / 2), width=A, height=P,
                    edgecolor='black', facecolor='skyblue', alpha=0.6)
    ax.add_patch(bulbo)

    ax.set_xlim(-A, A)
    ax.set_ylim(-P * 1.1, 5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xlabel("Ancho (cm)")
    ax.set_ylabel("Profundidad (cm)")
    ax.set_title("Perfil estimado del bulbo húmedo")
    ax.set_aspect('equal')
    st.pyplot(fig)
