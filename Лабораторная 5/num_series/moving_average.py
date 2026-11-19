from typing import List, Sequence
import time
from collections import deque

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

def simple_moving_average_deque(data: Sequence[float], window: int) -> List[float]:
    """SMA с использованием deque (двусторонней очереди)."""
    check_window(window, len(data))
    result: List[float] = []
    d: deque[float] = deque()
    running_sum = 0.0
    for x in data:
        d.append(x)
        running_sum += x
        if len(d) > window:
            running_sum -= d.popleft()
        if len(d) == window:
            result.append(running_sum / window)
    return result

def benchmark_moving_average(
    data: Sequence[float],
    window: int,
    repeats: int = 1000,
) -> dict:
    """Замеряет среднее время выполнения SMA для реализаций на list и deque.

    Возвращает словарь с ключами 'list' и 'deque' (время в секундах).
    """
    check_window(window, len(data))

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average(data, window)
    t_list = (time.perf_counter() - t0) / repeats

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average_deque(data, window)
    t_deque = (time.perf_counter() - t0) / repeats

    return {"list": t_list, "deque": t_deque}

def wma(data: Sequence[float], window: int) -> List[float]:
    """Взвешенная скользящая средняя (WMA) с окном window."""
    check_window(window, len(data))
    weights = list(range(1, window + 1))
    w_sum = sum(weights)
    result: List[float] = []
    for i in range(window - 1, len(data)):
        chunk = data[i - window + 1 : i + 1]
        result.append(sum(x * w for x, w in zip(chunk, weights)) / w_sum)
    return result