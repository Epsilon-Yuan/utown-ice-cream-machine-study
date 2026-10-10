#!/usr/bin/env python3
"""Estimate the geometric success probability from attempt-level CSV data."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Return a two-sided Wilson score interval for a binomial proportion."""
    p_hat = successes / trials
    z2 = z * z
    denominator = 1.0 + z2 / trials
    center = (p_hat + z2 / (2.0 * trials)) / denominator
    half_width = (
        z
        * math.sqrt(p_hat * (1.0 - p_hat) / trials + z2 / (4.0 * trials * trials))
        / denominator
    )
    return max(0.0, center - half_width), min(1.0, center + half_width)


def load_attempts(path: Path) -> list[int]:
    """Read one success (1) or failure (0) value per paid attempt."""
    outcomes: list[int] = []
    with path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or "success" not in reader.fieldnames:
            raise ValueError("CSV must have a 'success' column")
        for line_number, row in enumerate(reader, start=2):
            value = (row.get("success") or "").strip()
            if value not in {"0", "1"}:
                raise ValueError(f"Line {line_number}: success must be 0 or 1")
            outcomes.append(int(value))
    return outcomes


def report(path: Path, play_price: float, tub_value: float) -> int:
    if not path.exists():
        print(f"Error: data file not found: {path}", file=sys.stderr)
        return 2
    try:
        attempts = load_attempts(path)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not attempts:
        print("No observations found. Add one row per attempt; no empirical estimate was computed.")
        return 0

    trials = len(attempts)
    successes = sum(attempts)
    p_hat = successes / trials
    p_low, p_high = wilson_interval(successes, trials)

    print(f"Attempts: {trials}")
    print(f"Successes: {successes}")
    print(f"Estimated p: {p_hat:.4f}")
    print(f"95% Wilson interval for p: [{p_low:.4f}, {p_high:.4f}]")

    if p_hat == 0:
        expected_plays = math.inf
        expected_low = 1.0 / p_high if p_high > 0 else math.inf
        expected_high = math.inf
        print("Estimated expected plays: unbounded (no successes observed)")
    else:
        expected_plays = 1.0 / p_hat
        expected_low = 1.0 / p_high
        expected_high = 1.0 / p_low if p_low > 0 else math.inf
        print(f"Estimated expected plays until a win (1/p): {expected_plays:.2f}")

    if math.isfinite(expected_low) and math.isfinite(expected_high):
        print(f"Transformed 95% interval for expected plays: [{expected_low:.2f}, {expected_high:.2f}]")
    else:
        print(f"Transformed 95% interval for expected plays: [{expected_low:.2f}, infinity)")

    if math.isfinite(expected_plays):
        print(f"Estimated expected spend: ${play_price * expected_plays:.2f}")
    if tub_value > 0:
        print(f"Break-even success probability for a ${tub_value:.2f} tub: {play_price / tub_value:.4f}")
    print("Assumption: attempts are independent and have a constant success probability.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", nargs="?", type=Path, default=Path("data/attempts_template.csv"))
    parser.add_argument("--play-price", type=float, default=1.0, help="Cost per attempt (default: $1)")
    parser.add_argument("--tub-value", type=float, default=6.0, help="Comparison value (default: $6)")
    args = parser.parse_args()
    if args.play_price < 0 or args.tub_value < 0:
        parser.error("prices and values must be non-negative")
    return report(args.csv_path, args.play_price, args.tub_value)


if __name__ == "__main__":
    raise SystemExit(main())
