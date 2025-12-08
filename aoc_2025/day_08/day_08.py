import math
from dataclasses import dataclass


@dataclass
class Point3D:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __hash__(self):
        return hash((self.x, self.y, self.z))


def get_distance(p1: Point3D, p2: Point3D) -> float:
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2)


class Pair:
    def __init__(self, a: Point3D, b: Point3D):
        self.left = a
        self.right = b
        self.distance = get_distance(a, b)

    def intersect(self, other) -> bool:
        return self.left in (other.left, other.right) or self.right in (
            other.left,
            other.right,
        )

    def __repr__(self) -> str:
        return f"({self.left}, {self.right})"


def get_pairs(points: list[Point3D]) -> list[Pair]:
    pairs = []
    for i, p_1 in enumerate(points):
        for p_2 in points[i + 1 :]:
            pairs.append(Pair(p_1, p_2))
    return sorted(pairs, key=lambda p: p.distance)


def belong_to_group(group, pair) -> bool:
    return any(group_pair.intersect(pair) for group_pair in group)


def add_pair(circuits: list[list[Pair]], pair: Pair) -> list[list[Pair]]:
    first_circuit_idx = None
    second_circuit_idx = None
    for idx, circuit in enumerate(circuits):
        if belong_to_group(circuit, pair):
            if first_circuit_idx is None:
                first_circuit_idx = idx
            else:
                second_circuit_idx = idx
                break
    if second_circuit_idx is not None:
        circuits[first_circuit_idx].extend(circuits[second_circuit_idx])
        circuits[first_circuit_idx].append(pair)
        circuits.pop(second_circuit_idx)
    elif first_circuit_idx is not None:
        circuits[first_circuit_idx].append(pair)
    else:
        circuits.append([pair])
    return circuits


def part_one(points: list[Point3D]) -> int:
    pairs = get_pairs(points)[:1000]
    circuits = []
    for pair in pairs:
        circuits = add_pair(circuits, pair)

    circuits_sizes = []
    for circuit in circuits:
        unique_points = set([x for p in circuit for x in (p.left, p.right)])
        circuits_sizes.append(len(unique_points))
    return math.prod(sorted(circuits_sizes, reverse=True)[:3])


def part_two(points: list[Point3D]) -> int:
    pairs = get_pairs(points)
    circuits = []
    nbr_points = len(points)
    last_pair = None

    for pair in pairs:
        circuits = add_pair(circuits, pair)
        last_pair = pair
        if len(circuits) == 1:
            unique_points = set([x for p in circuits[0] for x in (p.left, p.right)])
            if len(unique_points) == nbr_points:
                return last_pair.left.x * last_pair.right.x
    raise ValueError("No solution found for part two")


def parse_input(filename: str) -> list[Point3D]:
    points = []
    with open(filename) as f:
        for line in f.readlines():
            x, y, z = [int(c) for c in line.split(",")]
            points.append(Point3D(x, y, z))
    return points


def main():
    points = parse_input("input_part_1.txt")
    result_1 = part_one(points)
    print(f"Result part 1: {result_1}")

    points = parse_input("input_part_2.txt")
    result_2 = part_two(points)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
