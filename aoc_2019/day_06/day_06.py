from collections import defaultdict, deque


def count_orbits(orbits: dict[str, list[str]], current_orbit: str, dist: int) -> int:
    count = dist
    for orbit in orbits.get(current_orbit, []):
        count += count_orbits(orbits, orbit, dist + 1)
    return count


def part_one(orbits: dict[str, list[str]]) -> int:
    return count_orbits(orbits, "COM", 0)


def get_path_len(came_from: dict[str, str | None], orbit: str | None) -> int:
    path = 0
    while orbit:
        path += 1
        orbit = came_from[orbit]
    return path - 3  # We remove the goal, end, and extra step


def bfs(orbits: dict[str, list[str]], start: str, goal: str) -> int:
    queue = deque([start])
    came_from: dict[str, str | None] = {start: None}
    while queue:
        current_orbit = queue.popleft()
        if current_orbit == goal:
            return get_path_len(came_from, current_orbit)
        for orbit in orbits.get(current_orbit, []):
            if orbit not in came_from:
                came_from[orbit] = current_orbit
                queue.append(orbit)
    raise ValueError("No path found")


def part_two(orbits: dict[str, list[str]]) -> int:
    two_way_dict = defaultdict(list)
    for key, value in orbits.items():
        for orbit in value:
            two_way_dict[key].append(orbit)
            two_way_dict[orbit].append(key)

    return bfs(two_way_dict, "YOU", "SAN")


def parse_input(filename: str) -> dict[str, list[str]]:
    orbits = defaultdict(list)
    with open(filename) as f:
        for line in f.readlines():
            left, right = line.strip().split(")")
            orbits[left].append(right)
    return orbits


def main():
    orbits = parse_input("input_part_1.txt")
    result_1 = part_one(orbits)
    print(f"Result part 1: {result_1}")

    orbits = parse_input("input_part_2.txt")
    result_2 = part_two(orbits)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
