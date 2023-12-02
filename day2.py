import re

file_path = "data/day2_input.txt"


def parse(line):
    matches = re.findall("^Game (\\d+): ", line)
    assert len(matches) > 0

    id = int(matches[0])

    line = re.sub("^Game (\\d+): ", "", line)
    cubes = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for s in line.split("; "):  # e.g. s = 3 blue, 4 red
        for t in s.split(", "):  # e.g. t = "3 blue"
            num, color = t.split(" ")
            assert color in cubes
            if int(num) > cubes[color]:
                cubes[color] = int(num)
    return id, cubes


def solve1():
    output = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            id, cubes = parse(line.strip())
            if cubes["red"] <= 12 and cubes["green"] <= 13 and cubes["blue"] <= 14:
                output = output + id

    return output


def solve2():
    output = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            id, cubes = parse(line.strip())
            output = output + cubes["red"] * cubes["green"] * cubes["blue"]

    return output


print(f"Q1: {solve1()}")
print(f"Q2: {solve2()}")
