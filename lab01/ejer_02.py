print("DISTANCIA RECORRIDA CON ACELERACIoN\n")

v = int(input("Ingresa la velocidad inicial (m/s): "))
a = int(input("Ingresa la aceleracion (m/s^2): "))
t = int(input("Ingresa el tiempo (s): "))

d = v * t + ( a * t * t ) / 2

print(f"\nLa distancia recorrida es {d} m\n")