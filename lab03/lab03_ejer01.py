import math

print("FUERZA EJERCIDA SOBRE UN CUERPO\n")

m = float(input("Ingresa la masa del cuerpo (kg): "))
print("Ingresa la aceleración a la que está sometido el cuerpo (m/s^2)")
ax = float(input("En el eje x: "))
ay = float(input("En el eje y: "))
az = float(input("En el eje z: "))

Fx = m * ax
Fy = m * ay
Fz = m * az
a = math.sqrt(ax**2 + ay**2 + az**2)
F = math.sqrt(Fx**2 + Fy**2 + Fz**2)

print(f"La suma de las fuerzas que afectan al cuerpo en el eje x es de {Fx} N")
print(f"La suma de las fuerzas que afectan al cuerpo en el eje y es de {Fy} N")
print(f"La suma de las fuerzas que afectan al cuerpo en el eje z es de {Fz} N")

print(f"\nEl modulo de la aceleracion que afecta al cuerpo es {a} m/s^2")
print(f"El modulo de la fuerza que afecta al cuerpo es {F} N\n")

