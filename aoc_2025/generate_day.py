import argparse
from pathlib import Path


def generate_day(day: int):
    """Generate directory structure for a given day."""
    day_str = f"{day:02d}"
    day_dir = Path(__file__).parent / f"day_{day_str}"

    # Create directory
    day_dir.mkdir(exist_ok=True)
    print(f"Created directory: {day_dir}")

    # Create Python file
    python_file = day_dir / f"day_{day_str}.py"
    python_template = f'''def part_one(data):
    pass


def part_two(data):
    pass


def parse_input(filename: str):
    with open(filename) as f:
        return f.read().strip()


def main():
    data = parse_input("input_part_1.txt")
    result_1 = part_one(data)
    print(f"Result part 1: {{result_1}}")

    data = parse_input("input_part_2.txt")
    result_2 = part_two(data)
    print(f"Result part 2: {{result_2}}")


if __name__ == "__main__":
    main()
'''
    python_file.write_text(python_template)
    print(f"Created file: {python_file}")

    # Create input files
    input_part_1 = day_dir / "input_part_1.txt"
    input_part_1.write_text("")
    print(f"Created file: {input_part_1}")

    input_part_2 = day_dir / "input_part_2.txt"
    input_part_2.write_text("")
    print(f"Created file: {input_part_2}")

    print(f"\nDay {day_str} structure generated successfully!")
    print(f"Next steps:")
    print(f"  1. Add your input to input_part_1.txt and input_part_2.txt")
    print(f"  2. Implement part_one() and part_two() in day_{day_str}.py")
    print(f"  3. Run with: cd day_{day_str} && uv run day_{day_str}.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Advent of Code day structure"
    )
    parser.add_argument(
        "day",
        type=int,
        help="Day number (1-12)",
        choices=range(1, 13),
    )
    args = parser.parse_args()
    generate_day(args.day)
