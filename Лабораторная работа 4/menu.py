"""
Меню выбора режима обработки через match-case.
"""
from __future__ import annotations
from consts import*

def show_menu() -> None:
    """Вывести меню выбора среды"""
    print("\nВыберите рабочую среду:")
    print("1 - вода")
    print("2 - масло")
    print("3 - воздух")
    print("0 - выход")

def select_medium() -> tuple[float, float,str] | None:
    """
    Циклически запрашивать среду.

    Использует match-case для маршрутизации.
    Возвращает None, если выбран выход (0)
    """
    while True:
        choice = input("Введите номер среды (0-3):").strip()
        match choice:
            case "1":
                return RHO_WATER, MU_WATER, "вода"
            case "2":
                return RHO_OIL, MU_OIL, "масло"
            case "3":
                 return RHO_AIR, MU_AIR, "воздух"
            case "0":
                return None
            case _:
                print("Ошибка: неверный пункт меню.")
        

