import math
import matplotlib.pyplot as plt


# Funkcje testowe wykorzystywane w całkowaniu
def f1(x): return x ** 2
def f2(x): return x * math.exp(-x)
def f3(x): return math.sin(x)
def f4(x): return math.exp(-x) * (x ** 3 + 2)

# Słownik z funkcjami i ich nazwami do wyboru w menu
functions = {
    '1': ('x^2', f1),
    '2': ('x * exp(-x)', f2),
    '3': ('sin(x)', f3),
    '4': ('exp(-x) * (x^3 + 2)', f4),
}

def simpson_weighted(f, a, b, n):
    """
    Oblicza wartość całki ∫_a^b e^{-x} * f(x) dx metodą Simpsona
    - Całkujemy z wagą e^{-x}, więc f(x) mnożone jest przez e^{-x} w każdym punkcie
    - Dla każdego z n podprzedziałów stosujemy klasyczny wzór Simpsona
    """
    h = (b - a) / n  # Długość pojedynczego podprzedziału
    result = 0.0

    for i in range(n):
        x0 = a + i * h          # Lewy koniec przedziału
        x1 = x0 + h / 2         # Środek przedziału
        x2 = x0 + h             # Prawy koniec przedziału
        result += (h / 6) * (
            math.exp(-x0) * f(x0) +
            4 * math.exp(-x1) * f(x1) +
            math.exp(-x2) * f(x2)
        )

    return result


def adaptive_simpson(f, a, b, eps=1e-6, initial_n=4, max_n=1024):
    """
    Oblicza wartość całki na przedziale [a, b] metodą Simpsona
    - W adaptacyjny sposób zwiększa liczbę podziałów, aż różnica między kolejnymi przybliżeniami
      będzie mniejsza niż zadana dokładność eps
    """
    n = initial_n
    prev_result = simpson_weighted(f, a, b, n)

    while n <= max_n:
        n *= 2
        current_result = simpson_weighted(f, a, b, n)
        if abs(current_result - prev_result) < eps:
            return current_result, n
        prev_result = current_result

    return prev_result, n  # Zwraca ostatnie najlepsze przybliżenie



def integrate_to_infinity(f, eps=1e-6, delta=1.0, initial_n=2):
    """
    Przybliża całkę ∫_0^∞ e^{-x} * f(x) dx
    - Przedział [0, ∞) dzielony jest na fragmenty [a, a+δ]
    - Całka liczona jest fragmentami, aż wkład z kolejnego fragmentu będzie mniejszy niż eps
    """
    a = 0.0
    total = 0.0
    interval_counts = []

    while True:
        part_result, used_n = adaptive_simpson(f, a, a + delta, eps / 10, initial_n)

        if abs(part_result) < eps:
            break  # Uznajemy, że dalszy wkład do całki jest pomijalny

        total += part_result
        a += delta
        interval_counts.append(used_n)

    max_intervals = max(interval_counts) if interval_counts else 0
    return total, max_intervals


# Zbiór gotowych węzłów i wag dla n-punktowej kwadratury Gaussa-Laguerre’a
gauss_laguerre_nodes_weights = {
    2: ([0.585786, 3.41421], [0.853553, 0.146447]),
    3: ([0.415775, 2.29428, 6.28995], [0.711093, 0.278518, 0.0103893]),
    4: ([0.322548, 1.74576, 4.53662, 9.39507], [0.603154, 0.357419, 0.0388881, 0.000539295]),
    5: ([0.26356, 1.4134, 3.59643, 7.08581, 12.6408], [0.521756, 0.398667, 0.0759424, 0.00361176, 2.33699e-05]),
}

def gauss_laguerre(f, n):
    """
    Oblicza wartość całki ∫_0^∞ e^{-x} f(x) dx za pomocą kwadratury Gaussa-Laguerre’a
    - Wagi i węzły uwzględniają już funkcję wagową e^{-x}
    - Całka ≈ ∑ w_i * f(x_i)
    """
    nodes, weights = gauss_laguerre_nodes_weights[n]
    return sum(w * f(x) for x, w in zip(nodes, weights))

def plot_results(f, fname):
    """
    Rysuje wykres funkcji podcałkowej: e^{-x} * f(x)
    - Pokazuje, jak zachowuje się funkcja tłumiona przez wagę
    """
    x_vals = [x * 0.1 for x in range(100)]
    y_vals = [math.exp(-x) * f(x) for x in x_vals]

    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label=r"$e^{-x} \cdot f(x)$")
    plt.title(f"Wykres funkcji podcałkowej ({fname})")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    print("Wybierz funkcję do całkowania:")
    for key in functions:
        print(f"{key}: {functions[key][0]}")

    choice = input("Twój wybór: ").strip()
    fname, f = functions.get(choice, functions['1'])

    eps = float(input("Podaj dokładność dla metody Simpsona (np. 1e-6): "))
    initial_n = int(input("Podaj początkową liczbę podziałów (np. 4): "))
    n_gauss = int(input("Podaj liczbę węzłów do Gauss-Laguerre (2–5): "))

    print("\n--- Obliczanie ---")
    result_simpson, max_intervals = integrate_to_infinity(f, eps, initial_n=initial_n)
    result_gauss = gauss_laguerre(f, n_gauss)

    print(f"\nWybrana funkcja: {fname}")
    print(f"[Simpson z wagą e^(-x)] Wynik: {result_simpson:.10f}")
    print(f"Maksymalna liczba podziałów: {max_intervals}")
    print(f"[Gauss-Laguerre, {n_gauss} węzłów] Wynik: {result_gauss:.10f}")
    print(f"Różnica między wynikami: {abs(result_simpson - result_gauss):.10e}")

    plot_results(f, fname)



def auto_test_all_functions():
    """
    Automatycznie porównuje metody Simpsona i Gauss-Laguerre’a
    dla wszystkich dostępnych funkcji testowych
    """
    eps = 1e-6
    initial_n = 4
    gauss_nodes_list = [2, 3, 4, 5]

    print("\n=== AUTOMATYCZNE PORÓWNANIE WSZYSTKICH FUNKCJI ===\n")
    for key, (fname, f) in functions.items():
        print(f"Funkcja: {fname}")
        result_simpson, max_intervals = integrate_to_infinity(f, eps, initial_n=initial_n)
        print(f"  Simpson (ε={eps}): {result_simpson:.10f}")
        print(f"  Max podziałów (Simpson): {max_intervals}")
        for n in gauss_nodes_list:
            result_gauss = gauss_laguerre(f, n)
            diff = abs(result_simpson - result_gauss)
            print(f"  Gauss-Laguerre (n={n}): {result_gauss:.10f} | Różnica: {diff:.2e}")
        print("-" * 50)



def menu():
    print("\n=== MENU PROGRAMU ===")
    print("1: Ręczny wybór funkcji i parametrów")
    print("2: Automatyczne porównanie wszystkich funkcji (test)")
    print("0: Wyjście")

    while True:
        choice = input("Wybierz opcję (0–2): ").strip()
        if choice == '1':
            main()
        elif choice == '2':
            auto_test_all_functions()
        elif choice == '0':
            print("Zakończono program.")
            break
        else:
            print("Niepoprawna opcja. Spróbuj ponownie.")



if __name__ == "__main__":
    menu()
