from collections import defaultdict

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


def solve2():
    cards_dict = defaultdict(int)
    card_num = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            card_num = card_num + 1
            cards_dict[card_num] = cards_dict[card_num] + 1

            splitted = line.strip().split()
            sep_index = splitted.index("|")
            winning_numbers = set(splitted[2:sep_index])
            numbers = splitted[sep_index + 1 :]
            scratchcard_num = card_num
            for number in numbers:
                if number in winning_numbers:
                    scratchcard_num = scratchcard_num + 1
                    cards_dict[scratchcard_num] = (
                        cards_dict[scratchcard_num] + cards_dict[card_num]
                    )
    return sum(cards_dict.values())


print(f"Q1: {solve1()}")
print(f"Q2: {solve2()}")
