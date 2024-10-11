import math

print("VELOCIDAD ORBITAL\n")

G = 6.674 * 10**-11
M = float(input("Ingresa la masa del cuerpo alrededor del cual orbita tu planeta (10^24 kg): "))
r = float(input("Ingresa el radio de la orbita (10^6 m): "))
T = float(input("Ingrese el periodo orbital (s): "))

# Velocidad basada en el periodo orbital (MRU)
vpo = (2 * math.pi * r * 10**6) / T

# Velocidad basada en la gravitacion (Estatica)
vg = math.sqrt((G * M * 10**24) / (r * 10**6))

print(f"\nLa velocidad orbital usando MRU es {vpo} m/s\n")
print(f"La velocidad orbital usando Estatica es {vg} m/s\n")