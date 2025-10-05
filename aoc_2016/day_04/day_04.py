import re
from collections import Counter
from dataclasses import dataclass


@dataclass
class Room:
    name: str
    sector_id: int
    checksum: str

    def is_valid(self) -> bool:
        letters = list(self.name.replace("-", ""))
        # We sort the letters before because in `most_common`,
        # elements with equal counts are ordered in the order first encountered
        letters.sort()
        counter = Counter(letters)
        for i, (letter, occurrences) in enumerate(counter.most_common(5)):
            if letter != self.checksum[i]:
                return False
        return True

    def get_decrypted_name(self) -> str:
        """from https://stackoverflow.com/a/1185809"""
        output = []
        for word in self.name.split("-"):
            output += [
                "".join(
                    map(
                        lambda c: chr(
                            ord("a") + (ord(c) - ord("a") + self.sector_id) % 26
                        ),
                        word,
                    )
                )
            ]
        return " ".join(output)


def part_one(rooms: list[Room]) -> int:
    return sum(room.sector_id for room in rooms if room.is_valid())


def part_two(rooms: list[Room]) -> int:
    for room in rooms:
        if room.is_valid():
            decrypted = room.get_decrypted_name()
            if "northpole" in decrypted:
                return room.sector_id
    raise ValueError("North Pole objects storage not found")


def parse_input(file_path: str) -> list[Room]:
    room_pattern = re.compile(r"([\D]+)-(\d+)\[(\D+)\]")
    rooms = []
    with open(file_path) as f:
        for line in f.readlines():
            if match := room_pattern.match(line):
                room = Room(match.group(1), int(match.group(2)), match.group(3))
                rooms.append(room)
    return rooms


def main():
    rooms = parse_input("input_part_1.txt")
    result_1 = part_one(rooms)
    print(f"Result part 1: {result_1}")

    rooms = parse_input("input_part_2.txt")
    result_2 = part_two(rooms)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
