from collections import Counter


def part_one(message: list[str]) -> str:
    corrected_message = ""
    rotated_message = list(zip(*message[::-1]))
    for line in rotated_message:
        count = Counter(line)
        corrected_message += count.most_common(1)[0][0]
    return corrected_message


def part_two(message: list[str]) -> str:
    corrected_message = ""
    rotated_message = list(zip(*message[::-1]))
    for line in rotated_message:
        count = Counter(line)
        corrected_message += count.most_common()[-1][0]
    return corrected_message


def main():
    with open("input_part_1.txt") as f:
        message = [line.strip() for line in f.readlines()]
        result_1 = part_one(message)
        print(f"Result part 1: {result_1}")

    with open("input_part_2.txt") as f:
        message = [line.strip() for line in f.readlines()]
        result_2 = part_two(message)
        print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
