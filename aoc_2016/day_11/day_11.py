import re
from collections import deque
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Floor:
    microchips: set[str]
    generators: set[str]

    def is_safe(self) -> bool:
        return not (self.generators and (self.microchips - self.generators))

    def copy(self) -> "Floor":
        return Floor(
            microchips=self.microchips.copy(), generators=self.generators.copy()
        )

    def is_empty(self):
        return not self.microchips and not self.generators

    def __hash__(self) -> int:
        return hash((frozenset(self.microchips), frozenset(self.generators)))


@dataclass
class Building:
    floors: list[Floor]
    current_floor: int

    def is_solved(self):
        return (
            self.floors[0].is_empty()
            and self.floors[1].is_empty()
            and self.floors[2].is_empty()
        )

    def copy(self) -> "Building":
        return Building([f.copy() for f in self.floors], self.current_floor)

    def is_safe(self) -> bool:
        return all(f.is_safe() for f in self.floors)

    def get_moves(self):
        for microchip in self.floors[self.current_floor].microchips:
            yield {microchip}, set()
        for microchips in combinations(self.floors[self.current_floor].microchips, 2):
            yield set(microchips), set()
        for generator in self.floors[self.current_floor].generators:
            yield set(), {generator}
        for generators in combinations(self.floors[self.current_floor].generators, 2):
            yield set(), set(generators)

        for microchip in self.floors[self.current_floor].microchips:
            set_microchip = {microchip}
            for generator in self.floors[self.current_floor].generators:
                set_generator = {generator}
                yield set_microchip, set_generator

    def get_state_from_move(
        self, direction: int, microchips: set[str], generators: set[str]
    ) -> "Building":
        new_state = Building(
            [f.copy() for f in self.floors],
            self.current_floor + direction,
        )
        new_state.floors[self.current_floor].microchips -= microchips
        new_state.floors[self.current_floor].generators -= generators
        new_state.floors[new_state.current_floor].microchips |= microchips
        new_state.floors[new_state.current_floor].generators |= generators
        return new_state

    def get_possible_moves(self):
        should_go_down = False
        for i in range(0, self.current_floor):
            if not self.floors[i].is_empty():
                should_go_down = True
                break

        for chips, gens in self.get_moves():
            if self.current_floor > 0 and should_go_down:
                state = self.get_state_from_move(-1, chips, gens)
                if state.is_safe():
                    yield state
            if self.current_floor < 3:
                state = self.get_state_from_move(1, chips, gens)
                if state.is_safe():
                    yield state

    def get_generic_state(self) -> tuple[int, tuple[tuple[int, int], ...]]:
        chips_position = {}
        generators_position = {}
        for i, floor in enumerate(self.floors):
            for microchip in floor.microchips:
                chips_position[microchip] = i
            for generator in floor.generators:
                generators_position[generator] = i
        element_names = chips_position.keys()
        pairs = list()
        for element_name in element_names:
            pairs.append(
                (chips_position[element_name], generators_position[element_name])
            )
        return self.current_floor, tuple(pairs)

    def __hash__(self) -> int:
        return hash(self.get_generic_state())

    def __eq__(self, other) -> bool:
        return self.get_generic_state() == other.get_generic_state()


def get_path_length(
    came_from: dict[Building, Building | None],
    start: Building,
    goal: Building,
) -> int:
    length = 0
    current = goal
    while current != start:
        length += 1
        current = came_from[current]
    return length


def bfs(start: Building) -> int:
    frontier = deque()
    frontier.append(start)
    came_from = dict()
    came_from[start] = None

    while frontier:
        current_building = frontier.popleft()
        for neighbor in current_building.get_possible_moves():
            if neighbor not in came_from:
                frontier.append(neighbor)
                came_from[neighbor] = current_building
                if neighbor.is_solved():
                    return get_path_length(came_from, start, neighbor)

    raise ValueError(f"No path found from {start}")


def part_one(building: Building) -> int:
    return bfs(building)


def part_two(building: Building) -> int:
    building.floors[0].microchips.add("elerium")
    building.floors[0].microchips.add("dilithium")
    building.floors[0].generators.add("elerium")
    building.floors[0].generators.add("dilithium")
    return bfs(building)


def parse_input(file_path: str) -> Building:
    floor_pattern = re.compile(r"The \w+ floor contains ([\w \-,]+)")
    elements_pattern = re.compile(r"(\w+)(?:-compatible)? (generator|microchip)")

    with open(file_path) as f:
        lines = f.readlines()
    building = Building([Floor(set(), set()) for _ in range(4)], 0)

    for floor, line in enumerate(lines):
        match = floor_pattern.match(line)
        raw_elements = match.group(1)
        for match in elements_pattern.finditer(raw_elements):
            if match.group(2) == "generator":
                building.floors[floor].generators.add(match.group(1))
            else:
                building.floors[floor].microchips.add(match.group(1))
    return building


def main():
    building = parse_input("input_part_1.txt")
    result_1 = part_one(building)
    print(f"Result part 1: {result_1}")

    building = parse_input("input_part_2.txt")
    result_2 = part_two(building)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
