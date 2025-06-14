import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils.ode_solver import resolver_edo

st.set_page_config(page_title="Solver EDO Genérica", layout="centered")
st.title("Solución Numérica de una Ecuación Diferencial Ordinaria (EDO)")

st.markdown(r"""
\[
\frac{dy}{dt} = f(t, y)
\]
""")

presets = {
    "Personalizada": "",
    "Enfriamiento de Newton": "-k*(y - Tamb)",
    "Crecimiento Logístico": "r * y * (1 - y / K)",
    "Decaimiento exponencial": "-λ * y",
    "Sinusoidal amortiguado": "-0.1*y + sin(t)"
}

seleccion = st.selectbox("Selecciona un modelo predefinido o escribe el tuyo", list(presets.keys()))

if seleccion == "Personalizada":
    funcion_str = st.text_input("Escribe f(t, y):", value="-0.5 * (y - 25)")
else:
    funcion_str = st.text_input("f(t, y)", value=presets[seleccion])

col1, col2 = st.columns(2)
with col1:
    t0 = st.number_input("Tiempo inicial (t₀)", value=0.0)
    tf = st.number_input("Tiempo final (t_f)", value=10.0)
with col2:
    y0 = st.number_input("Condición inicial y(t₀)", value=1.0)
    num_puntos = st.slider("Número de puntos", 50, 1000, 200)

st.markdown("### Parámetros opcionales (si aplican)")
k = st.number_input("k", value=0.5)
Tamb = st.number_input("Temperatura ambiente (Tamb)", value=25.0)
r = st.number_input("r (tasa de crecimiento)", value=1.0)
K = st.number_input("K (capacidad de carga)", value=10.0)
λ = st.number_input("λ (constante de decaimiento)", value=1.0)

funcion_str = funcion_str.replace("k", str(k))
funcion_str = funcion_str.replace("Tamb", str(Tamb))
funcion_str = funcion_str.replace("r", str(r))
funcion_str = funcion_str.replace("K", str(K))
funcion_str = funcion_str.replace("λ", str(λ))

if st.button("Resolver EDO"):
    try:
        t, y = resolver_edo(funcion_str, t0, tf, y0, num_puntos)
        fig, ax = plt.subplots()
        ax.plot(t, y, label="y(t)", color="blue")
        ax.set_title("Solución Numérica")
        ax.set_xlabel("t")
        ax.set_ylabel("y(t)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
        with st.expander("Detalles de la solución"):
            st.code(f"f(t, y) = {funcion_str}")
            st.write(f"Intervalo: t ∈ [{t0}, {tf}] con {num_puntos} puntos")
            st.write(f"Condición inicial: y({t0}) = {y0}")
    except Exception as e:
        st.error(f"Ocurrió un error al resolver la EDO:\n\n{e}")

