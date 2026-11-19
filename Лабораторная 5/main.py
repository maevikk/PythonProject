"""Точка входа: обработка числовых рядов (генерация / чтение / сохранение)."""

from __future__ import annotations

import argparse
import csv
import sys
from typing import List, Optional, Tuple

from num_series import (
    benchmark_moving_average,
    centered_moving_average,
    discrete_series,
    exponential_moving_average,
    load_series_auto,
    quartiles_iqr,
    random_series,
    save_series_json,
    simple_moving_average,
    sine_series,
    summarize,
    trend_series,
    wma,
)

def build_series(kind: str, n: int, seed: int) -> List[float]:
    """Генерирует ряд заданного типа."""
    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10, frequency=2, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0, step=1.0, noise=0.5, seed=seed)
    if kind == "discrete":
        return discrete_series(n=n, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")

def obtain_series(args: argparse.Namespace) -> Tuple[List[float], str]:
    """Возвращает (ряд, описание источника)."""
    if args.load:
        data = load_series_auto(args.load)
        return data, f"файл: {args.load}"
    data = build_series(args.kind, args.n, args.seed)
    return data, f"сгенерирован ({args.kind}, n={args.n}, seed={args.seed})"

def export_series_csv(path: str, data: List[float]) -> None:
    """Экспорт ряда в CSV: столбцы i, value. Ошибки нормализуются в ValueError."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["i", "value"])
            for i, v in enumerate(data):
                w.writerow([i, v])
    except OSError as err:
        raise ValueError(f"Не удалось записать CSV {path}: {err}") from err

def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    print(f"\n{title} (n={len(values)}):")
    print(" " + " ".join(fmt.format(v) for v in values))

def print_header(source: str) -> None:
    print("=" * 60)
    print(f"Источник данных: {source}")
    print("-" * 60)

def print_stats(stats: dict) -> None:
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана               : {stats['median']:>10.4f}")
    print(f"Размах (max - min)    : {stats['spread']:>10.4f}")
    print(f"min / max             : {stats['min']:>10.4f} / {stats['max']:.4f}")

def print_quartiles(q1: float, q3: float, iqr: float) -> None:
    print(f"Q1                    : {q1:>10.4f}")
    print(f"Q3                    : {q3:>10.4f}")
    print(f"IQR (Q3 - Q1)         : {iqr:>10.4f}")

def print_footer() -> None:
    print("=" * 60)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Пример: python main.py --kind sine --n 20 --save data/s.json",
    )
    parser.add_argument(
        "--kind",
        choices=["random", "sine", "trend", "discrete"],
        default="discrete",
        help="тип генерируемого ряда",
    )
    parser.add_argument(
        "--n", type=int, default=1000, help="количество точек в ряде"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="зерно ГПСЧ для воспроизводимости"
    )
    parser.add_argument(
        "--load",
        metavar="PATH",
        help="загрузить ряд из файла (.json/.txt/.csv); отменяет --kind/--n/--seed",
    )
    parser.add_argument(
        "--save", metavar="PATH", help="сохранить ряд в JSON-файл"
    )
    parser.add_argument(
        "--export", metavar="FILE", help="экспортировать ряд в CSV (i, value)"
    )
    parser.add_argument(
        "--window", type=int, default=10, help="размер окна для скользящей средней"
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.3,
        help="коэффициент сглаживания для EMA, 0 < alpha <= 1",
    )
    parser.add_argument(
        "--benchmark", action="store_true",
        help="замерить время выполнения SMA для list и deque",
    )
    return parser

def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        data, source = obtain_series(args)
    except ValueError as err:
        print(f"Ошибка получения ряда: {err}", file=sys.stderr)
        return 1

    if args.save:
        meta = {"source": source}
        if not args.load:
            meta.update({"kind": args.kind, "seed": args.seed})
        try:
            save_series_json(data, args.save, meta=meta)
            print(f"[сохранено] {args.save} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка сохранения: {err}", file=sys.stderr)
            return 1

    if args.export:
        try:
            export_series_csv(args.export, data)
            print(f"[экспортировано] {args.export} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка экспорта: {err}", file=sys.stderr)
            return 1

    try:
        stats = summarize(data)
        q1, q3, iqr = quartiles_iqr(data)
        sma = simple_moving_average(data, args.window)
        wma_vals = wma(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
        cma = (
            centered_moving_average(data, args.window)
            if args.window % 2 == 1
            else None
        )
    except ValueError as err:
        print(f"Ошибка анализа: {err}", file=sys.stderr)
        return 1

    print_header(source)
    print_stats(stats)
    print_quartiles(q1, q3, iqr)
    print_series("Исходный ряд", data)
    print_series(f"SMA (window={args.window})", sma)
    print_series(f"WMA (window={args.window})", wma_vals)
    print_series(f"EMA (alpha={args.alpha})", ema)
    if cma is not None:
        print_series(f"Центрированное МА (window={args.window})", cma)
    if args.benchmark:
        print("-" * 60)
        print("Замер времени выполнения SMA (среднее за 1000 повторов):")
        timings = benchmark_moving_average(data, args.window, repeats=1000)
        print(f"  list : {timings['list']:.8f} c")
        print(f"  deque: {timings['deque']:.8f} c")
        if timings["deque"] > 0:
            print(f"  отношение (list/deque): {timings['list'] / timings['deque']:.2f}")
    print_footer()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())