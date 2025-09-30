from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int


def get_next_chunk(blacklist: list[Range]) -> tuple[Range, list[Range]]:
    min_start = min(blacklist, key=lambda r: r.start)
    cleared_blacklist = [n for n in blacklist if n != min_start]
    max_end = min_start.end
    check_for_change = True

    while check_for_change:
        check_for_change = False
        for idx, node in enumerate(cleared_blacklist):
            if node.start <= max_end + 1:  # This node is linked
                max_end = max(max_end, node.end)
                cleared_blacklist[idx] = None
                check_for_change = True
                break
        cleared_blacklist = [node for node in cleared_blacklist if node is not None]
    return Range(min_start.start, max_end), cleared_blacklist


def get_merged_blacklist(blacklist: list[Range]) -> list[Range]:
    clean_list = []

    while blacklist:
        chunk, blacklist = get_next_chunk(blacklist)
        clean_list.append(chunk)
    return clean_list


def part_one(blacklist: list[Range]) -> int:
    return get_merged_blacklist(blacklist)[0].end + 1


def part_two(blacklist: list[Range]) -> int:
    blacklist = get_merged_blacklist(blacklist)
    whitelist_nbr = 0
    prev_chunk = blacklist[0]
    for chunk in blacklist[1:]:
        whitelist_nbr += chunk.start - prev_chunk.end - 1
        prev_chunk = chunk
    whitelist_nbr += 4294967295 - prev_chunk.end
    return whitelist_nbr


def parse_input(file_path: str) -> list[Range]:
    blacklist = []
    with open(file_path) as f:
        for line in f:
            start, end = map(int, line.strip().split("-"))
            blacklist.append(Range(start=start, end=end))
    return blacklist


def main():
    blacklist = parse_input("input_part_1.txt")
    result_1 = part_one(blacklist)
    print(f"Result part 1: {result_1}")

    blacklist = parse_input("input_part_2.txt")
    result_2 = part_two(blacklist)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
