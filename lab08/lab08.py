import math

def bisection(f, a, b, tol=1e-5, max_iter=100):
    if f(a) * f(b) >= 0:
        print("La bisección no es posible en este intervalo.")
        return None
    iter_count = 0
    while (b - a) / 2 > tol and iter_count < max_iter:
        r = (a + b) / 2
        if f(r) == 0:
            break
        elif f(a) * f(r) < 0:
            b = r
        else:
            a = r
        iter_count += 1
    return (a + b) / 2

def newton_raphson(f, df, xi, tol=1e-5, max_iter=100):
    iter_count = 0
    while abs(f(xi)) > tol and iter_count < max_iter:
        dfx = df(xi)
        if dfx == 0:
            print(f"Error: La derivada en x = {xi} es cero, esta función no tiene solución por este método.")
            return None
        xi = xi - f(xi) / dfx
        iter_count += 1
    return xi

def newton_raphson_system_2d(f1, f2, jacobian, x0, y0, tol=1e-5, max_iter=100):
    x, y = x0, y0
    for i in range(max_iter):
        # Evaluar las funciones y el Jacobiano
        f1_val = f1(x, y)
        f2_val = f2(x, y)
        J = jacobian(x, y)
        
        # Calcular el determinante de la matriz Jacobiana
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        if abs(det) < 1e-10:  # Verificar si el Jacobiano es singular
            print("Error: La matriz Jacobiana es singular en esta iteración.")
            return None
        
        # Calcular las actualizaciones dx y dy usando la regla de Cramer
        dx = (f1_val * J[1][1] - f2_val * J[0][1]) / det
        dy = (f2_val * J[0][0] - f1_val * J[1][0]) / det
        
        # Actualizar x y y
        x -= dx
        y -= dy
        
        # Verificar convergencia
        if abs(dx) < tol and abs(dy) < tol:
            return x, y

    print("Error: El método no convergió en el número máximo de iteraciones.")
    return None

def falsa_posicion(f, a, b, tol=1e-5, max_iter=100):
    if f(a) * f(b) >= 0:
        print("La falsa posición no es posible en este intervalo.")
        return None
    iter_count = 0
    while abs(b - a) > tol and iter_count < max_iter:
        r = b - f(b) * (b - a) / (f(b) - f(a))
        if f(r) == 0:
            break
        elif f(a) * f(r) < 0:
            b = r
        else:   
            a = r
        iter_count += 1
    return r

def secante(f, xim1, xi, tol=1e-5, max_iter=100):
    iter_count = 0
    while abs(f(xi)) > tol and iter_count < max_iter:
        xiM1 = xi - f(xi) * (xi - xim1) / (f(xi) - f(xim1))
        xim1, xi = xi, xiM1
        iter_count += 1
    return xi

# 1. y = ln(x - 2)
f1 = lambda x: math.log(x - 2) if x > 2 else float('nan')
sol = bisection(f1, 2.5, 3.5)
print(f"1. La solución de y = ln(x - 2) es: {sol}")
# 2. y = e^(-x)
f2 = lambda x: math.exp(-x)
df2 = lambda x: -math.exp(-x)
sol = newton_raphson(f2, df2, 0.5)
print(f"2. La solución de y = e^(-x) es: {sol}")
# 3. y = e^x - x
f3 = lambda x: math.exp(x) - x
df3 = lambda x: math.exp(x) - 1
sol = newton_raphson(f3, df3, 0.5)
print(f"3. La solución de y = e^x - x es: {sol}")
# 4. y = (10 * e^(x/2)) * cos(2x)
f4 = lambda x: 10 * math.exp(x / 2) * math.cos(2 * x)
sol = falsa_posicion(f4, 0, 1)
print(f"4. La solución de y = (10 * e^(x/2)) * cos(2x) es: {sol}")
# 5. y = x^2 - 2
f5 = lambda x: x**2 - 2
df5 = lambda x: 2 * x
sol = newton_raphson(f5, df5, 1.5)
print(f"5. La solución de y = y = x^2 - 2 es: {sol}")
# 6. y = (x - 2)^(1/2)
f6 = lambda x: math.sqrt(x - 2) if x >= 2 else float('nan')
sol = secante(f6, 1.5, 2)
print(f"6. La solución de y = (x - 2)^(1/2) es: {sol}")
# 7. y = x * cos(y) + y * sin(x)
f71 = lambda x, y: x * math.cos(y) + y * math.sin(x) - y
f72 = lambda x, y: y  # Segunda función
# Jacobiano
jacobian = lambda x, y: [
    [math.cos(y) + y * math.cos(x), -x * math.sin(y) + math.sin(x) - 1],
    [0, 1]
]
sol = newton_raphson_system_2d(f1, f2, jacobian, 1.0, 1.0)
print(f"7. La solución de y = x * cos(y) + y * sin(x) es: {sol}")
# 8. y = 2 / x
f8 = lambda x: 2 / x if x != 0 else float('inf')
sol = bisection(lambda x: x**2 - 2, a=0.5, b=2)
print(f"8. La solución de y = 2 / x es: {sol}")