import math

def f1(x):
    return x**2  # Przykładowa funkcja

def f2(x):
    return x * math.exp(-x)  # e^{-x} * x, używana przy porównaniach

def f3(x):
    return math.sin(x)

# Możliwość dodania kolejnych funkcji
functions = {
    '1': f1,
    '2': f2,
    '3': f3,
}
def simpson_weighted(f, a, b, n):
    h = (b - a) / n
    result = 0.0

    for i in range(n):
        x0 = a + i * h
        x1 = x0 + h / 2
        x2 = x0 + h
        result += (h / 6) * (math.exp(-x0)*f(x0) + 4*math.exp(-x1)*f(x1) + math.exp(-x2)*f(x2))

    return result
def integrate_to_infinity(f, eps=1e-6, delta=1.0):
    a = 0.0
    total = 0.0

    while True:
        part = simpson_weighted(f, a, a + delta, 10)
        if abs(part) < eps:
            break
        total += part
        a += delta

    return total
gauss_laguerre_nodes_weights = {
    2: ([0.585786, 3.41421], [0.853553, 0.146447]),
    3: ([0.415775, 2.29428, 6.28995], [0.711093, 0.278518, 0.0103893]),
    4: ([0.322548, 1.74576, 4.53662, 9.39507], [0.603154, 0.357419, 0.0388881, 0.000539295]),
    5: ([0.26356, 1.4134, 3.59643, 7.08581, 12.6408], [0.521756, 0.398667, 0.0759424, 0.00361176, 2.33699e-05]),
}

def gauss_laguerre(f, n):
    nodes, weights = gauss_laguerre_nodes_weights[n]
    return sum(w * f(x) for x, w in zip(nodes, weights))

def main():
    print("Wybierz funkcję do całkowania:")
    for key in functions:
        print(f"{key}: {functions[key].__name__}")
    choice = input("Twój wybór: ").strip()
    f = functions.get(choice, f1)

    eps = float(input("Podaj dokładność dla metody Simpsona (np. 1e-6): "))
    n_gauss = int(input("Podaj liczbę węzłów do Gauss-Laguerre (2–5): "))

    print("\n--- Obliczanie ---")
    result_simpson = integrate_to_infinity(f, eps)
    result_gauss = gauss_laguerre(f, n_gauss)

    print(f"\n[Simpson z wagą e^(-x)] Wynik: {result_simpson}")
    print(f"[Gauss-Laguerre, {n_gauss} węzłów] Wynik: {result_gauss}")
    print(f"Różnica: {abs(result_simpson - result_gauss)}")
if __name__ == "__main__":
    main()
