import math

print("CONSERVACION DE LA ENERGIA MECANICA\n")
m = float(input("Ingrese la masa del objeto (kg): "))
h1 = float(input("Ingrese la altura inicial (m): "))
h2 = float(input("Ingrese la altura final (m): "))
v1 = float(input("Ingrese la velocidad inicial (m/s): "))
g = 9.8

EK1 = 0.5 * m * v1**2
EP1 = m * g * h1
EM1 = EK1 + EP1

v2 = math.sqrt(v1**2 + 2 * g * (h1 - h2))

EK2 = 0.5 * m * v2**2
EP2 = m * g * h2
EM2 = EK2 + EP2

print("\nRESULTADOS")
print("Momento 1:")
print(f"\tEnergía cinética inicial (EK1): {EK1:.2f} J")
print(f"\tEnergía potencial inicial (EP1): {EP1:.2f} J")
print(f"\tEnergía mecánica inicial (EM1): {EM1:.2f} J")
print("Momento 2:")
print(f"\tEnergía cinética final (EK2): {EK2:.2f} J")
print(f"\tEnergía potencial final (EP2): {EP2:.2f} J")
print(f"\tEnergía mecánica final (EM2): {EM2:.2f} J")

if math.isclose(EM1, EM2, rel_tol=1e-5):
    print("\nLa energía mecánica se conserva.")
else:
    print("\nLa energía mecánica no se conserva.")