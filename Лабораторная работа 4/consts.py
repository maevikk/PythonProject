"""Константы расчёта потерь давления в трубопроводе."""

from __future__ import annotations

# Имя файла журнала ошибок
LOG_FILE: str = "input_errors.log"

# Допустимые диапазоны параметров
L_MIN: float = 1.0
L_MAX: float = 1000.0

D_MIN: float = 10.0
D_MAX: float = 500.0

Q_MIN: float = 0.1
Q_MAX: float = 100.0

EPS_MIN: float = 0.0
EPS_MAX: float = 2.0

# Номера пунктов меню
M_WATER: str = "1"
M_OIL: str = "2"
M_AIR: str = "3"
M_EXIT: str = "0"

# Параметры воды
RHO_WATER: float = 1000.0
MU_WATER: float = 0.001

# Параметры масла
RHO_OIL: float = 900.0
MU_OIL: float = 0.05

# Параметры воздуха
RHO_AIR: float = 1.2
MU_AIR: float = 1.8e-5