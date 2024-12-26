import numpy as np
import matplotlib.pyplot as plt
import os

# Crear una carpeta para guardar los gráficos
output_folder = "graficos_funciones"
os.makedirs(output_folder, exist_ok=True)

# Definición de las funciones
functions = [
    {"name": "ln(x - 2)", "func": lambda x: np.log(x - 2), "range": (2.1, 10)},
    {"name": "e^(-x)", "func": lambda x: np.exp(-x), "range": (-5, 5)},
    {"name": "e^x - x", "func": lambda x: np.exp(x) - x, "range": (-2, 2)},
    {"name": "(10e^(x/2))cos(2x)", "func": lambda x: 10 * np.exp(x / 2) * np.cos(2 * x), "range": (-2, 2)},
    {"name": "x^2 - 2", "func": lambda x: x**2 - 2, "range": (-2, 2)},
    {"name": "sqrt(x - 2)", "func": lambda x: np.sqrt(x - 2), "range": (2.1, 10)},
    {"name": "2/x", "func": lambda x: 2 / x, "range": (0.1, 10)},
    {"name": "x*cos(y) + y*sin(x)", 
     "func": lambda x: np.array([x_i * np.cos(x_i) + np.sin(x_i) * x_i for x_i in x]), 
     "range": (-2, 2)}
]

# Generar gráficos
for i, item in enumerate(functions, start=1):
    func_name = item["name"]
    func = item["func"]
    x_range = item["range"]

    x = np.linspace(x_range[0], x_range[1], 500)
    try:
        y = func(x)
        plt.figure()
        plt.plot(x, y, label=f"y = {func_name}")
        plt.axhline(0, color='black', linestyle='--', linewidth=0.7)
        plt.title(f"Gráfico de {func_name}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        # Guardar el gráfico con nombres como equacion_1.png, equacion_2.png, etc.
        plt.savefig(f"{output_folder}/equacion_{i}.png")
        plt.close()
    except Exception as e:
        print(f"Error al graficar la ecuación {i} ({func_name}): {e}")

print(f"Gráficos guardados en la carpeta '{output_folder}'.")