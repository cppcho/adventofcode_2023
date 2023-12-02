import re

file_path = "data/day2_input.txt"


def parse(line: str) -> (int, bool):
    matches = re.findall("^Game (\\d+): ", line)
    assert len(matches) > 0

    id = int(matches[0])

    line = re.sub("^Game (\\d+): ", "", line)
    for s in line.split("; "):  # e.g. s = 3 blue, 4 red
        cubes = {
            "red": 12,
            "green": 13,
            "blue": 14,
        }

        for t in s.split(", "):  # e.g. t = "3 blue"
            num, color = t.split(" ")
            assert color in cubes
            cubes[color] = cubes[color] - int(num)
            if cubes[color] < 0:
                return id, False

    return id, True


def solve1():
    output = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            id, possible = parse(line.strip())
            if possible:
                output = output + id

    return output


print(f"Q1: {solve1()}")
