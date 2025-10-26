import re
from collections import defaultdict, deque


def compute_game(players: int, last_marble: int) -> int:
    current_player = 1
    scores = defaultdict(int)
    marbles = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            marbles.rotate(7)
            scores[current_player] += marble + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble)
        current_player = (current_player + 1) % players
    return max(scores.values())


def part_one(players: int, last_marble: int) -> int:
    return compute_game(players, last_marble)


def part_two(players: int, last_marble: int) -> int:
    return compute_game(players, last_marble * 100)


def parse_input(filename: str) -> tuple[int, int]:
    pattern = re.compile(r"(\d+) players; last marble is worth (\d+) points")
    with open(filename) as f:
        result = pattern.match(f.readline()).groups()
        return int(result[0]), int(result[1])


def main():
    players, last_marble = parse_input("input_part_1.txt")
    result_1 = part_one(players, last_marble)
    print(f"Result part 1: {result_1}")

    players, last_marble = parse_input("input_part_2.txt")
    result_2 = part_two(players, last_marble)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
