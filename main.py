import math


def calculate(L, d, Q, eps, rho, mu, medium):
    d_m = d / 1000

    v = (Q / 1000) / (math.pi * d_m ** 2 / 4)
    Re = rho * v * d_m / mu

    if Re < 1e4:
        lam = 0.3164 / Re ** 0.25
    else:
        lam = 0.11 * ((eps / 1000) / d_m + 68 / Re) ** 0.25

    dp = lam * (L / d_m) * rho * v ** 2 / 2

    if Re < 2300:
        regime = "ламинарный"
    elif Re <= 10000:
        regime = "переходный"
    else:
        regime = "турбулентный"

    result = (
        f"Среда: {medium}\n"
        f"Скорость потока v = {v:.3f} м/с\n"
        f"Число Рейнольдса Re = {Re:.2f}\n"
        f"Коэффициент сопротивления λ = {lam:.5f}\n"
        f"Потери давления Δp = {dp:.2f} Па\n"
        f"Потери давления Δp = {dp / 1000:.5f} кПа\n"
        f"Режим течения: {regime}"
    )

    return result


print("Расчёт потерь давления в трубопроводе")
print("1 — вода")
print("2 — масло")
print("3 — воздух")

try:
    choice = int(input("Выберите среду (1-3): "))

    if choice < 1 or choice > 3:
        result = "Ошибка: выберите среду от 1 до 3."
    else:
        match choice:
            case 1:
                rho = 1000
                mu = 0.001
                medium = "вода"
            case 2:
                rho = 900
                mu = 0.05
                medium = "масло"
            case 3:
                rho = 1.2
                mu = 1.8e-5
                medium = "воздух"

        L = float(input("Длина трубы L, м (1-1000): "))

        if L < 1 or L > 1000:
            result = "Ошибка: длина трубы должна быть от 1 до 1000 м."
        else:
            d = float(input("Диаметр трубы d, мм (10-500): "))

            if d < 10 or d > 500:
                result = "Ошибка: диаметр должен быть от 10 до 500 мм."
            else:
                Q = float(input("Расход Q, л/с (0.1-100): "))

                if Q < 0.1 or Q > 100:
                    result = "Ошибка: расход должен быть от 0.1 до 100 л/с."
                else:
                    eps = float(input("Шероховатость ε, мм (0-2): "))

                    if eps < 0 or eps > 2:
                        result = "Ошибка: шероховатость должна быть от 0 до 2 мм."
                    else:
                        result = calculate(
                            L, d, Q, eps, rho, mu, medium
                        )

except ValueError:
    result = "Ошибка: необходимо вводить числовые значения."

print(result)
