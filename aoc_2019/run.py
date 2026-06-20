import argparse
import importlib
from contextlib import chdir
from pathlib import Path


def run_day(day: int):
    with chdir(Path(__file__).parent / f"day_{day:02d}"):
        module = importlib.import_module(f"day_{day:02d}.day_{day:02d}")
        module.main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an Advent of Code day")
    parser.add_argument(
        "day",
        type=int,
        help="Day number (1-25)",
        choices=range(1, 26),
    )
    args = parser.parse_args()
    run_day(args.day)
