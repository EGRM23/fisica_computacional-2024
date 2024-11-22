print("FUERZA EN MRUV\n")

m = int(input("Ingresa la masa del cuerpo en movimiento (kg): "))
vi = int(input("Ingresa la velocidad inicial en (m/s): "))
vf = int(input("Ingresa la velocidad final en (m/s): "))
t = int(input("Ingresa el tiempo (s): "))

F = m * ((vf - vi) / t)

print(f"\nLa fuerza que actua sobre el movil al cambiar velocidad es {F} N\n")