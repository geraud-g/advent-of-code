from functools import cache


def count_paths(devices: dict[str, tuple[str, ...]], start: str, goal: str) -> int:
    if start == goal:
        return 1

    return sum(count_paths(devices, device, goal) for device in devices[start])


def part_one(devices: dict[str, tuple[str, ...]]) -> int:
    return count_paths(devices, "you", "out")


def count_paths_with_dac_and_fft(
    devices: dict[str, tuple[str, ...]], start: str, goal: str
) -> int:
    @cache
    def count_paths_with_dac_and_fft_cached(
        start: str, goal: str, saw_dac: bool = False, saw_fft: bool = False
    ) -> int:
        if start == "dac":
            saw_dac = True
        elif start == "fft":
            saw_fft = True
        if start == goal and saw_dac and saw_fft:
            return 1
        total = 0
        for next_device in devices.get(start, []):
            total += count_paths_with_dac_and_fft_cached(
                next_device, goal, saw_dac, saw_fft
            )
        return total

    return count_paths_with_dac_and_fft_cached(start, goal)


def part_two(devices: dict[str, tuple[str, ...]]) -> int:
    return count_paths_with_dac_and_fft(devices, "svr", "out")


def parse_input(filename: str) -> dict[str, tuple[str, ...]]:
    devices = dict()
    with open(filename) as f:
        for line in f.readlines():
            device, links = line.strip().split(":")
            devices[device] = tuple(links.strip().split())
    return devices


def main():
    devices = parse_input("input_part_1.txt")
    result_1 = part_one(devices)
    print(f"Result part 1: {result_1}")

    devices = parse_input("input_part_2.txt")
    result_2 = part_two(devices)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
