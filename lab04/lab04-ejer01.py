import math
from sympy import integrate, exp, sin, log, init_printing
from sympy.abc import x
import numpy as np

init_printing()
print("TRABAJO EJERCIDO POR UNA FUERZA VARIABLE\n")

f1 = 10 * exp(-x)  # Usando exp de SymPy
f2 = 5 * sin(x) + 3
f3 = 8 * log(x)
print("Función 1: F(x) = 10 * e^(-x)")
print("Función 2: F(x) = 5 * sin(x) + 3")
print("Función 3: F(x) = 8 * ln(x)")

print("\nIngresa el desplazamiento que tuvo el cuerpo en el eje x")
x1 = float(input("Posicion inicial (x1): "))
x2 = float(input("Posicion final (x2): "))

f1i = integrate(f1, (x,x1,x2))
f1s = sum(f1.subs(x, i) for i in range(int(x1), int(x2) + 1))
f1s = f1s.evalf()
d1 = abs((f1i - f1s) / f1i) * 100
f2i = integrate(f2, (x,x1,x2))
f2s = sum(f2.subs(x, i) for i in range(int(x1), int(x2) + 1))
f2s = f2s.evalf()
d2 = abs((f2i - f2s) / f2i) * 100
f3i = integrate(f3, (x,x1,x2))
f3s = sum(f3.subs(x, i) for i in range(int(x1), int(x2) + 1))
f3s = f3s.evalf()
d3 = abs((f3i - f3s) / f3i) * 100

print("\nResultados:")
print("Trabajo por la Función 1 (Integral)")
print(f"\tIntegral: {f1i:.4f} J")
print(f"\tSumatoria: {f1s:.4f} J")
print(f"\tDiferencia porcentual: {d1:.2f}%")
print("Trabajo por la Función 2 (Integral)")
print(f"\tIntegral: {f2i:.4f} J")
print(f"\tSumatoria: {f2s:.4f} J")
print(f"\tDiferencia porcentual: {d2:.2f}%")
print("Trabajo por la Función 3 (Integral)")
print(f"\tIntegral: {f3i:.4f} J")
print(f"\tSumatoria: {f3s:.4f} J")
print(f"\tDiferencia porcentual: {d3:.2f}%")