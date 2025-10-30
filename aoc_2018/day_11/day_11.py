def get_grid(serial_number: int) -> list[list[int]]:
    grid = []
    for y in range(1, 301):
        line = []
        for x in range(1, 301):
            rack_id = x + 10
            power = rack_id * y
            power += serial_number
            power *= rack_id
            power = (power // 100) % 10
            power -= 5
            line += [power]
        grid.append(line)
    return grid


def get_power_range_3(grid: list[list[int]], y: int, x: int) -> int:
    try:
        return (
            grid[y][x]
            + grid[y][x + 1]
            + grid[y][x + 2]
            + grid[y + 1][x]
            + grid[y + 1][x + 1]
            + grid[y + 1][x + 2]
            + grid[y + 2][x]
            + grid[y + 2][x + 1]
            + grid[y + 2][x + 2]
        )
    except IndexError:
        return 0


def part_one(serial_number: int) -> str:
    grid = get_grid(serial_number)
    max_power = float("-inf")
    coords = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            power = get_power_range_3(grid, y, x)
            if power > max_power:
                max_power = power
                coords = (x + 1, y + 1)
    return f"{coords[0]},{coords[1]}"


def get_power_range_and_size(
    grid: list[list[int]], y2: int, x2: int
) -> tuple[int, int]:
    last_computed = grid[y2][x2]
    max_power = last_computed
    max_power_size = 1
    square_size = 1

    while x2 + square_size - 1 < 300 and y2 + square_size - 1 < 300:
        try:
            current_computed = last_computed
            square_size += 1
            for y in range(0, square_size + 1):
                current_computed += grid[y2 + y][x2 + square_size]
            for x in range(0, square_size):
                current_computed += grid[y2 + square_size][x + x2]
            if current_computed > max_power:
                max_power = current_computed
                max_power_size = square_size
            last_computed = current_computed
        except IndexError:
            return max_power, max_power_size + 1
    return max_power, max_power_size + 1


def part_two(serial_number: int) -> str:
    grid = get_grid(serial_number)
    max_power = float("-inf")
    coords = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            power, square_size = get_power_range_and_size(grid, y, x)
            if power > max_power:
                max_power = power
                coords = (x + 1, y + 1, square_size)
    return f"{coords[0]},{coords[1]},{coords[2]}"


def parse_input(filename: str) -> int:
    with open(filename) as f:
        return int(f.readline())


def main():
    serial_number = parse_input("input_part_1.txt")
    result_1 = part_one(serial_number)
    print(f"Result part 1: {result_1}")

    serial_number = parse_input("input_part_2.txt")
    result_2 = part_two(serial_number)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
