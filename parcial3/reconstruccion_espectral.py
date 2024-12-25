import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.special import gamma

def tsallis_rnd(qv, Tqv, dim):
    """
    Genera números aleatorios siguiendo la distribución de Tsallis.
    
    Args:
        qv (float): Parámetro de visita (1 <= qv <= 3).
        Tqv (float): Temperatura de visita.
        dim (tuple): Dimensión del vector solución.
    
    Returns:
        np.ndarray: Vector de números aleatorios.
    """
    n = (3 - qv) / (qv - 1)
    s = np.sqrt(2 * (qv - 1)) / (Tqv ** (1 / (3 - qv)))
    
    X = np.random.normal(0, 1, dim)
    U = np.random.gamma(n / 2, 2, size=dim)
    Y = s * np.sqrt(U)
    Z = X / Y
    return Z

def gsa(fun, x0, l, u, qv=2.7, qa=-5, Imax=400):
    """
    Generalized Simulated Annealing (GSA) para minimizar una función objetivo.
    
    Args:
        fun (callable): Función objetivo.
        x0 (np.ndarray): Solución inicial.
        l (np.ndarray): Límites inferiores.
        u (np.ndarray): Límites superiores.
        qv (float): Parámetro de visita (1 <= qv <= 3).
        qa (float): Parámetro de aceptación (-5 <= qa <= -1).
        Imax (int): Número máximo de iteraciones.
    
    Returns:
        tuple: (xo, fo, tiempo) donde:
            xo (np.ndarray): Solución óptima.
            fo (float): Valor de la función objetivo en xo.
            tiempo (float): Tiempo de cálculo.
    """
    start_time = time.time()

    # Validación de parámetros
    if not (1 <= qv <= 3):
        raise ValueError("qv debe estar entre 1 y 3")
    if not (-5 <= qa <= -1):
        raise ValueError("qa debe estar entre -5 y -1")

    # Inicialización
    x = np.array(x0)
    fx = fun(x)
    xo, fo = x.copy(), fx
    dim = x.shape

    k = 1.38e-23

    # Iteraciones
    for t in range(1, Imax + 1):
        # Enfriamiento
        Tqv0 = Imax
        if qv == 1:
            Tqv = Tqv0 / np.log(1 + t)
        elif qv == 2:
            Tqv = Tqv0 / (1 + t)
        else:
            Tqv = Tqv0 * ((2 ** (qv - 1)) - 1) / (((1 + t) ** (qv - 1)) - 1)
        Tqa = Tqv / t

        # Generar nuevas soluciones
        for _ in range(Imax // 5):
            dx = tsallis_rnd(qv, Tqv, dim) * (u - l)
            x_new = np.clip(x + dx, l, u)

            # Evaluar la función objetivo
            fx_new = fun(x_new)
            delta_f = fx_new - fx

            # Probabilidad de aceptación
            if delta_f < 0:
                Pa = 1
            else:
                Pa = 1 / ((1 + (qa - 1) * delta_f / (k * Tqa)) ** (1 / (qa - 1)))

            # Aceptar o rechazar
            if delta_f < 0 or np.random.rand() < Pa:
                x, fx = x_new, fx_new

            # Actualizar solución óptima
            if fx < fo:
                xo, fo = x.copy(), fx

    elapsed_time = time.time() - start_time
    return xo, fo, elapsed_time

def transmission_model(x, d, T_exp, mu_m0, C, mu_mi):
    """
    Modelo de transmisión para ajustar los datos experimentales.

    Args:
        x (np.ndarray): Parámetros del modelo (a, b, v, r).
        d (np.ndarray): Grosor del material.
        T_exp (np.ndarray): Datos experimentales de transmisión.
        mu_m0 (float): Coeficiente de atenuación másico nominal.
        C (np.ndarray): Abundancia relativa de líneas características.
        mu_mi (np.ndarray): Coeficientes de atenuación másicos para las líneas características.

    Returns:
        float: Error cuadrático entre los datos experimentales y el modelo.
    """
    a, b, v, r = x
    T_model = (
        r * ((a * b) / ((d + a) * (d + b))) ** v * np.exp(-mu_m0 * d)
        + (1 - r) * np.sum(C[:, None] * np.exp(-np.outer(mu_mi, d)), axis=0)
    )
    return np.linalg.norm(T_exp - T_model)

def reconstruct_spectrum(x, E, mu_m0, C, mu_mi):
    """
    Reconstruir el espectro de energía basado en los parámetros ajustados.

    Args:
        x (np.ndarray): Parámetros ajustados (a, b, v, r).
        E (np.ndarray): Energías del espectro.
        mu_m0 (float): Coeficiente de atenuación másico nominal.
        C (np.ndarray): Abundancia relativa de líneas características.
        mu_mi (np.ndarray): Coeficientes de atenuación másicos para las líneas características.

    Returns:
        np.ndarray: Espectro de energía reconstruido F(E).
    """
    a, b, v, r = x

    # Espectro continuo (bremsstrahlung)
    Fb = (
        r * (np.sqrt(np.pi) * (a * b) ** 2 / gamma(v))
        * (((mu_mi - mu_m0) / (a - b)) ** (v - 0.5))
        * np.exp(-0.5 * (a + b) * (mu_mi - mu_m0))
        * np.i0(0.5 * (a - b) * (mu_mi - mu_m0))
    )

    # Espectro de líneas características
    Fc = (1 - r) * np.sum(C[:, None] * np.exp(-mu_mi[:, None] * E), axis=0)

    # Espectro total
    F = Fb + Fc
    F /= np.max(F)
    return F

def calculate_hvl(d, T_model):
    """
    Calcula la Capa Semirreductora (HVL) a partir de la curva de transmisión.

    Args:
        d (np.ndarray): Grosor del material.
        T_model (np.ndarray): Curva de transmisión modelada.

    Returns:
        float: Valor de HVL (grosor donde T = 0.5).
    """
    hvl_index = np.argmin(np.abs(T_model - 0.5))
    return d[hvl_index]

def main():
    # Datos simulados
    d = np.linspace(0.1, 1.0, 10)  # Grosor del material (cm)
    T_exp = np.exp(-0.5 * d)  # Transmisión experimental simulada
    mu_m0 = 0.5  # Coeficiente de atenuación
    C = np.array([0.3, 0.2, 0.1])  # Abundancia relativa de líneas características
    mu_mi = np.array([0.4, 0.6, 0.8])  # Coeficientes de atenuación másicos para líneas características

    # Función objetivo
    def fun_to_minimize(x):
        return transmission_model(x, d, T_exp, mu_m0, C, mu_mi)

    # Parámetros iniciales
    x0 = np.array([1, 1, 0.5, 0.5])
    l = np.array([0, 0, 0, 0])
    u = np.array([10, 10, 1, 1])

    # Optimización
    start_time = time.time()
    xo, fo, elapsed_time = gsa(fun_to_minimize, x0, l, u)
    print("Parámetros ajustados:", xo)
    print("Error mínimo:", fo)
    print("Tiempo de cálculo:", elapsed_time, "segundos")

    # Curva de transmisión modelada
    T_model = (
        xo[3] * ((xo[0] * xo[1]) / ((d + xo[0]) * (d + xo[1]))) ** xo[2] * np.exp(-mu_m0 * d)
        + (1 - xo[3]) * np.sum(C[:, None] * np.exp(-np.outer(mu_mi, d)), axis=0)
    )

    # Cálculo de la HVL
    hvl = calculate_hvl(d, T_model)
    print("HVL calculada:", hvl, "cm")

    # Reconstrucción del espectro
    E = np.linspace(1, 100, 100)
    spectrum = reconstruct_spectrum(xo, E, mu_m0, C, mu_mi)

    # Resultados
    plt.figure(figsize=(12, 6))

    # Transmisión
    plt.subplot(1, 2, 1)
    plt.plot(d, T_exp, 'o', label="Datos experimentales")
    plt.plot(d, T_model, '-', label="Modelo ajustado")
    plt.axhline(0.5, color='r', linestyle='--', label="T = 0.5 (HVL)")
    plt.axvline(hvl, color='g', linestyle='--', label=f"HVL = {hvl:.2f} cm")
    plt.xlabel("Grosor del material (cm)")
    plt.ylabel("Transmisión")
    plt.legend()
    plt.title("Curva de Transmisión")

    # Espectro
    plt.subplot(1, 2, 2)
    plt.plot(E, spectrum, '-b')
    plt.xlabel("Energía (keV)")
    plt.ylabel("Intensidad Normalizada")
    plt.title("Espectro de Energía Reconstruido")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()