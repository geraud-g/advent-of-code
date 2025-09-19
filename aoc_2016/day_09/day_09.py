import re

MARKER_PATTERN = re.compile("\((\d+)x(\d+)\)")


def part_one(compressed_file: str) -> int:
    output_len = 0
    first_parenthesis = compressed_file.find("(")
    output_len += first_parenthesis
    idx = first_parenthesis

    while idx < len(compressed_file):
        if match := MARKER_PATTERN.match(compressed_file, idx):
            char_nbr = int(match.group(1))
            to_repeat = int(match.group(2))
            output_len += char_nbr * to_repeat
            idx = match.end() + char_nbr
        else:
            output_len += 1
            idx += 1
    return output_len


def part_two(compressed_file: str) -> int:
    output_len = 0
    first_parenthesis = compressed_file.find("(")
    output_len += first_parenthesis
    idx = first_parenthesis

    while idx < len(compressed_file):
        if match := MARKER_PATTERN.match(compressed_file, idx):
            char_nbr = int(match.group(1))
            to_repeat = int(match.group(2))
            segment = compressed_file[match.end() : match.end() + char_nbr]
            segment_size = part_two(segment) * to_repeat
            output_len += segment_size
            idx = match.end() + char_nbr
        else:
            output_len += 1
            idx += 1
    return output_len


def parse_input(file_path: str) -> str:
    with open(file_path) as f:
        return f.readline().strip()


def main():
    compressed_file = parse_input("input_part_1.txt")
    result_1 = part_one(compressed_file)
    print(f"Result part 1: {result_1}")

    compressed_file = parse_input("input_part_2.txt")
    result_2 = part_two(compressed_file)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
