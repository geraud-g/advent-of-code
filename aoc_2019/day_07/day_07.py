from itertools import permutations

from lib.intcode import Process


def part_one(intcode: list[int]) -> int:
    max_signal_value = -1
    for sequence in permutations(range(5)):
        last_output = 0
        for setting in sequence:
            program = Process(intcode.copy(), program_input=[setting, last_output])
            program.run_until_output()
            last_output = program.output[-1]
        max_signal_value = max(last_output, max_signal_value)
    return max_signal_value


def part_two(intcode: list[int]) -> int:
    max_signal_value = -1
    for sequence in permutations(range(5, 10)):
        processes = [Process(intcode.copy()) for _ in range(5)]
        for idx, setting in enumerate(sequence):
            processes[idx].add_input(setting)

        last_output = 0
        current_process_idx = 0
        while not processes[-1].exited:
            processes[current_process_idx].add_input(last_output)
            processes[current_process_idx].run_until_output()
            last_output = processes[current_process_idx].output[-1]
            current_process_idx = (current_process_idx + 1) % 5
        max_signal_value = max(processes[-1].output[-1], max_signal_value)

    return max_signal_value


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(c) for c in f.readline().split(",")]


def main():
    intcode = parse_input("input_part_1.txt")
    result_1 = part_one(intcode)
    print(f"Result part 1: {result_1}")

    intcode = parse_input("input_part_2.txt")
    result_2 = part_two(intcode)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
