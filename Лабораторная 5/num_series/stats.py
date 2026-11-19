from typing import Dict, Sequence

def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")

def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)

def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0

def spread(data: Sequence[float]) -> float:
    """Размах ряда: max - min."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))

def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Сводный отчёт: count, mean, median, spread, min, max."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
    }

from typing import Tuple

def _median_of_sorted(vals: Sequence[float]) -> float:
    m = len(vals)
    mid = m // 2
    if m % 2 == 1:
        return float(vals[mid])
    return (float(vals[mid - 1]) + float(vals[mid])) / 2.0

def quartiles_iqr(data: Sequence[float]) -> Tuple[float, float, float]:
    """Вычисляет Q1, Q3 и IQR = Q3 - Q1 вручную без numpy."""
    if not data:
        raise ValueError("Ряд пуст")
    s = sorted(float(x) for x in data)
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        lower = s[:mid]
        upper = s[mid:]
    else:
        lower = s[:mid]
        upper = s[mid + 1 :]
    q1 = _median_of_sorted(lower) if lower else float(s[0])
    q3 = _median_of_sorted(upper) if upper else float(s[-1])
    iqr = q3 - q1
    return q1, q3, iqr