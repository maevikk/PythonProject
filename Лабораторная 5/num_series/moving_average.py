from typing import List, Sequence

def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")

def check_window(window: int, n: int) -> None:
    """Проверка корректности окна: целое число, 1 <= window <= n."""
    if isinstance(window, bool) or not isinstance(window, int) or window < 1:
        raise ValueError(f"Окно должно быть целым числом >= 1 (получено: {window!r})")
    if window > n:
        raise ValueError(f"Окно ({window}) не может быть больше длины ряда ({n})")

def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Простая скользящая средняя (SMA) через бегущую сумму O(n)."""
    _ensure_not_empty(data)
    n = len(data)
    check_window(window, n)

    running = sum(data[:window])
    result = [running / window]
    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result

def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированная скользящая средняя (окно нечётное, выровнена по центру)."""
    _ensure_not_empty(data)
    n = len(data)
    check_window(window, n)
    if window % 2 == 0:
        raise ValueError(f"Для центрированной MA окно должно быть нечётным (получено: {window})")

    half = window // 2
    result = []
    for i in range(half, n - half):
        window_slice = data[i - half : i + half + 1]
        result.append(sum(window_slice) / window)
    return result

def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """Экспоненциальная скользящая средняя (EMA), 0 < alpha <= 1."""
    _ensure_not_empty(data)
    if not (0 < alpha <= 1):
        raise ValueError(f"Коэффициент alpha должен быть в (0, 1] (получено: {alpha})")

    ema = [float(data[0])]
    for i in range(1, len(data)):
        ema.append(alpha * data[i] + (1.0 - alpha) * ema[i - 1])
    return ema