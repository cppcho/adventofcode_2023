file_path = "data/day4_input.txt"


def solve1():
    output = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            splitted = line.strip().split()
            sep_index = splitted.index("|")
            winning_numbers = set(splitted[2:sep_index])
            numbers = splitted[sep_index + 1 :]
            score = 0
            for number in numbers:
                if number in winning_numbers:
                    if score == 0:
                        score = 1
                    else:
                        score = score * 2
            output = output + score

    return output


print(f"Q1: {solve1()}")
