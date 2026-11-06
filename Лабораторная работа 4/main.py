from __future__ import annotations
from menu import show_menu, select_medium
from validation import input_length, input_diameter, input_flow, input_roughness
from operations import flow_speed, reynolds_number, resistance_coefficient, pressure_loss, flow_regime

def main() -> None:
    """Главный сценарий программы."""
    print("=== Расчёт потерь давления в трубопроводе ===")
    while True:
        show_menu()
        medium_data = select_medium()
        if medium_data is None:
            print("Работа завершена.")
            break

        try:
            rho, mu, medium = medium_data

            # Ввод и проверка параметров
            L = input_length()
            d = input_diameter()
            Q = input_flow()
            eps = input_roughness()

            # Расчёт скорости потока
            v = flow_speed(Q, d)
            # Расчёт числа Рейнольдса
            Re = reynolds_number(rho, v, d, mu)
            # Расчёт коэффициента сопротивления
            lam = resistance_coefficient(Re, eps, d)
            # Расчёт потерь давления
            dp = pressure_loss(lam, L, d, rho, v)
            # Определение режима течения
            regime = flow_regime(Re)

            # Вывод результатов
            print("\nРезультаты расчёта")
            print(f"Среда: {medium}")
            print(f"Скорость потока = {v:.3f} м/с")
            print(f"Число Рейнольдса = {Re:.2f}")
            print(f"Коэффициент сопротивления = {lam:.5f}")
            print(f"Потери давления = {dp:.2f} Па")
            print(f"Потери давления = {dp / 1000:.5f} кПа")
            print(f"Режим течения: {regime}")

        except (ValueError, ZeroDivisionError) as error:
            message = f"Ошибка расчёта: {error}"
            print(message)
            log_error(message)

if __name__ == "__main__":
    main()