import numpy as np
from scipy.integrate import odeint

def construir_funcion(funcion_str: str):
    funciones_permitidas = {
        'np': np,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'exp': np.exp,
        'log': np.log,
        'sqrt': np.sqrt,
        'abs': np.abs,
        'pi': np.pi,
        'e': np.e
    }
    try:
        codigo = compile(funcion_str, "<string>", "eval")
        return lambda y, t: eval(codigo, funciones_permitidas, {'t': t, 'y': y})
    except Exception as e:
        raise ValueError(f"Error al construir la función f(t, y): {e}")

def resolver_edo(funcion_str: str, t0: float, tf: float, y0: float, num_puntos: int):
    t = np.linspace(t0, tf, num_puntos)
    f = construir_funcion(funcion_str)
    y = odeint(f, y0, t)
    return t, y.ravel()

