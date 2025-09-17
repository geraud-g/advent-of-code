import re

Hypernet = tuple[str, ...]
Supernet = tuple[str, ...]


def support_tls(supernet: Supernet) -> bool:
    for chunk in supernet:
        for idx in range(len(chunk) - 3):
            first_pair = chunk[idx] + chunk[idx + 1]
            if first_pair[0] == first_pair[1]:
                continue
            second_pair = chunk[idx + 3] + chunk[idx + 2]
            if first_pair == second_pair:
                return True
            idx += 1
    return False


def part_one(ips: list[tuple[Supernet, Hypernet]]) -> int:
    return sum(
        support_tls(supernet) and not support_tls(hypernet)
        for supernet, hypernet in ips
    )


def support_ssl(supernet: Supernet, hypernet: Hypernet) -> bool:
    for chunk in supernet:
        for idx in range(len(chunk) - 2):
            aba = chunk[idx] + chunk[idx + 1] + chunk[idx + 2]
            if not (aba[0] == aba[2] and aba[0] != aba[1]):
                continue
            bab = aba[1] + aba[0] + aba[1]
            if any(bab in x for x in hypernet):
                return True
    return False


def part_two(ips: list[tuple[Supernet, Hypernet]]) -> int:
    return sum(support_ssl(supernet, hypernet) for supernet, hypernet in ips)


def parse_input(file_path: str) -> list[tuple[Supernet, Hypernet]]:
    with open(file_path) as f:
        lines = f.readlines()
    pattern = re.compile("\[([^]]+)]|([^\[\]]+)")
    output = []
    for line in lines:
        supernet = []
        hypernet = []
        for m in pattern.finditer(line):
            if m.group(1):
                hypernet.append(m.group(1))
            else:
                supernet.append(m.group(2))
        output.append((tuple(supernet), tuple(hypernet)))
    return output


def main():
    ips = parse_input("input_part_1.txt")
    result_1 = part_one(ips)
    print(f"Result part 1: {result_1}")

    ips = parse_input("input_part_2.txt")
    result_2 = part_two(ips)
    print(f"Result part 1: {result_2}")


if __name__ == "__main__":
    main()
