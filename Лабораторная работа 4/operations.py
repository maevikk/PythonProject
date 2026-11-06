"""
Операции расчёта потерь давления в трубопроводе.
"""

from __future__ import annotations
import math

def flow_speed(
    Q: float,
    d: float
) -> float:
    """
    Рассчитать скорость потока v, м/с.
    Args:
        Q: расход, л/с.
        d: диаметр трубы, мм.
    Returns:
        Скорость потока, м/с.
    """
    d_m = d / 1000.0
    Q_m = Q / 1000.0
    return Q_m / (math.pi * d_m ** 2 / 4.0)

def reynolds_number(
    rho: float,
    v: float,
    d: float,
    mu: float
) -> float:
    """
    Рассчитать число Рейнольдса Re.
    Args:
        rho: плотность среды, кг/м³.
        v: скорость потока, м/с.
        d: диаметр трубы, мм.
        mu: динамическая вязкость, Па·с.
    Returns:
        Число Рейнольдса.
    """
    d_m = d / 1000.0
    return rho * v * d_m / mu

def resistance_coefficient(
    Re: float,
    eps: float,
    d: float
) -> float:
    """
    Рассчитать коэффициент сопротивления lambda.
    Args:
        Re: число Рейнольдса.
        eps: шероховатость, мм.
        d: диаметр трубы, мм.
    Returns:
        Коэффицент сопротивления.
    """
    d_m = d / 1000.0
    eps_m = eps / 1000.0
    if Re < 1e4:
        lam = 0.3164 / Re ** 0.25
    else:
        lam = 0.11 * (
            eps_m / d_m + 68.0 / Re
        ) ** 0.25
    return lam

def pressure_loss(
    lam: float,
    L: float,
    d: float,
    rho: float,
    v: float
) -> float:
    """
    Рассчитать потери давления dp, Па.
    Args:
        lam: коэффициент сопротивления.
        L: длина трубы, м.
        d: диаметр трубы, мм.
        rho: плотность среды, кг/м³.
        v: скорость потока, м/с.

    Returns:
        Потери давления, Па.
    """
    d_m = d / 1000.0
    return lam * (L / d_m) * rho * v ** 2 / 2.0

def flow_regime(
    Re: float
) -> str:
    """
    Определить режим течения через if-elif-else.
    Returns:
        Название режима течения.
    """
    if Re < 2300:
        return "ламинарный"
    elif Re <= 10000:
        return "переходный"
    else:
        return "турбулентный"