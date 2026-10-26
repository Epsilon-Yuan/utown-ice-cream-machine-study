#!/usr/bin/env python3
"""Estimate p from preselected sessions all followed through their first win."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def load_waiting_times(path: Path) -> list[int]:
    """Read one positive play count through the first win per completed session."""
    waiting_times: list[int] = []
    with path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or "attempts_to_first_win" not in reader.fieldnames:
            raise ValueError("CSV must have an 'attempts_to_first_win' column")
        for line_number, row in enumerate(reader, start=2):
            value = (row.get("attempts_to_first_win") or "").strip()
            try:
                attempts = int(value)
            except ValueError as exc:
                raise ValueError(f"Line {line_number}: attempts_to_first_win must be a positive integer") from exc
            if attempts < 1:
                raise ValueError(f"Line {line_number}: attempts_to_first_win must be a positive integer")
            waiting_times.append(attempts)
    return waiting_times


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=Path("data/completed_sessions_template.csv"),
    )
    parser.add_argument("--play-price", type=float, default=1.0, help="Cost per play (default: $1)")
    parser.add_argument("--tub-value", type=float, default=6.0, help="Comparison value (default: $6)")
    args = parser.parse_args()
    if args.play_price < 0 or args.tub_value < 0:
        parser.error("prices and values must be non-negative")
    if not args.csv_path.exists():
        print(f"Error: data file not found: {args.csv_path}", file=sys.stderr)
        return 2

    try:
        waiting_times = load_waiting_times(args.csv_path)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not waiting_times:
        print("No completed sessions found; no empirical estimate was computed.")
        return 0

    sessions = len(waiting_times)
    total_plays = sum(waiting_times)
    p_hat = sessions / total_plays
    expected_plays = 1.0 / p_hat

    print(f"Completed sessions: {sessions}")
    print(f"Total plays in completed sessions: {total_plays}")
    print(f"Estimated p (sessions / total plays): {p_hat:.4f}")
    print(f"Estimated expected plays until a win (1/p): {expected_plays:.2f}")
    print(f"Estimated expected spend: ${args.play_price * expected_plays:.2f}")
    if args.tub_value > 0:
        print(f"Break-even success probability for a ${args.tub_value:.2f} tub: {args.play_price / args.tub_value:.4f}")
    print("Assumption: plays are independent and have a constant success probability.")
    print("Use only sessions selected before their outcomes and followed through their first win.")
    print("If any selected sessions were unfinished, retain all outcomes in the attempt-level method.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
