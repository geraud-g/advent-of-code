import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Record:
    ts: datetime


@dataclass(frozen=True)
class Guard(Record):
    id: int


@dataclass(frozen=True)
class WakesUp(Record):
    pass


@dataclass(frozen=True)
class FallsAsleep(Record):
    pass


RE_GUARD = re.compile(
    r"^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] Guard #(\d+) begins shift$"
)
RE_FALLS = re.compile(r"^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] falls asleep$")
RE_WAKES = re.compile(r"^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] wakes up$")


def parse_input(filename: str) -> list[Record]:
    events: list[Record] = []

    with open(filename, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            if m := RE_GUARD.match(line):
                year, month, day, hour, minute, gid = m.groups()
                ts = datetime(int(year), int(month), int(day), int(hour), int(minute))
                events.append(Guard(ts=ts, id=int(gid)))
            elif m := RE_FALLS.match(line):
                year, month, day, hour, minute = m.groups()
                ts = datetime(int(year), int(month), int(day), int(hour), int(minute))
                events.append(FallsAsleep(ts=ts))
            elif m := RE_WAKES.match(line):
                year, month, day, hour, minute = m.groups()
                ts = datetime(int(year), int(month), int(day), int(hour), int(minute))
                events.append(WakesUp(ts=ts))
            else:
                raise ValueError(f"Unrecognized line: {line!r}")

    events.sort(key=lambda r: r.ts)
    return events


def get_guard_sleep_patterns(records: list[Record]) -> dict[int, dict[int, int]]:
    records = sorted(records, key=lambda r: r.ts)
    current_guard_id = -1
    last_sleep_time = None
    sleeps = defaultdict(lambda: defaultdict(int))

    for record in records:
        match record:
            case Guard(ts=ts, id=guard_id):
                last_sleep_time = None
                current_guard_id = guard_id
            case WakesUp(ts=ts):
                if last_sleep_time:
                    current = last_sleep_time
                    while current < ts:
                        sleeps[current_guard_id][current.minute] += 1
                        current += timedelta(minutes=1)
                    last_sleep_time = None
            case FallsAsleep(ts=ts):
                last_sleep_time = ts
            case _:
                raise ValueError(f"Unrecognized record: {record!r}")
    return sleeps


def part_one(records: list[Record]) -> int:
    sleeps = get_guard_sleep_patterns(records)
    guard_asleep = max(sleeps.keys(), key=lambda g: sum(sleeps[g].values()))
    max_minute = max(sleeps[guard_asleep].items(), key=lambda i: i[1])
    return guard_asleep * max_minute[0]


def part_two(records: list[Record]) -> int:
    sleeps = get_guard_sleep_patterns(records)
    max_time_asleep = None
    guard_asleep = None
    for guard_id, minutes in sleeps.items():
        max_minute = max(minutes.items(), key=lambda i: i[1])
        if not max_time_asleep or max_minute[1] > max_time_asleep[1]:
            guard_asleep = guard_id
            max_time_asleep = max_minute
    return guard_asleep * max_time_asleep[0]


def main():
    claims = parse_input("input_part_1.txt")
    result_1 = part_one(claims)
    print(f"Result part 1: {result_1}")

    claims = parse_input("input_part_2.txt")
    result_2 = part_two(claims)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
