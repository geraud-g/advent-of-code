import enum
import re
from collections import defaultdict, deque
from dataclasses import dataclass


class BotType(enum.Enum):
    BOT = "bot"
    OUTPUT = "output"

@dataclass
class Behavior:
    lower_to: str
    higher_to: str


@dataclass
class Bot:
    values: list[int]
    id: str | None = None
    behavior: Behavior | None = None
    type: BotType | None = BotType.OUTPUT


def part_one(bots: defaultdict[str, Bot], values_to_compare: list[int] | None) -> int | None:
    bots_to_process = deque()
    for bot in bots.values():
        if bot.type != BotType.BOT:
            continue
        if len(bot.values) == 2:
            bots_to_process.append(bot)

    while bots_to_process:
        bot = bots_to_process.popleft()
        if values_to_compare and sorted(bot.values) == values_to_compare:
            return int(bot.id.split(" ")[1])
        low_value, high_value = sorted(bot.values)
        bot.values.clear()
        low_target = bots[bot.behavior.lower_to]
        high_target = bots[bot.behavior.higher_to]
        low_target.values.append(low_value)
        high_target.values.append(high_value)
        if low_target.type == BotType.BOT and len(low_target.values) == 2:
            bots_to_process.append(low_target)
        if high_target.type == BotType.BOT and len(high_target.values) == 2:
            bots_to_process.append(high_target)
    return None


def part_two(bots: defaultdict[str, Bot]) -> int:
    part_one(bots, None)
    return bots["output 0"].values[0] * bots["output 1"].values[0] * bots["output 2"].values[0]


def parse_input(file_path: str) -> defaultdict[str, Bot]:
    initialization_pattern = re.compile(r"value (\d+) goes to ((?:bot|output) \d+)")
    behavior_pattern = re.compile(r"((?:bot|output) \d+) gives low to ((?:bot|output) \d+) and high to ((?:bot|output) \d+)")
    with open(file_path) as f:
        lines = f.readlines()

    bots = defaultdict(lambda: Bot(list()))
    for line in lines:
        if match := initialization_pattern.match(line):
            bot_id = match.group(2)
            bots[bot_id].values.append(int(match.group(1)))
            bots[bot_id].id = bot_id
            bots[bot_id].type = BotType.BOT
        elif match := behavior_pattern.match(line):
            bots[match.group(1)].behavior = Behavior(match.group(2), match.group(3))
            bots[match.group(1)].id = match.group(1)
            bots[match.group(1)].type = BotType.BOT
    return bots


def main():
    instructions = parse_input("input_part_1.txt")
    result_1 = part_one(instructions, [17, 61])
    print(f"Result part 1: {result_1}")

    instructions = parse_input("input_part_2.txt")
    result_2 = part_two(instructions)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
