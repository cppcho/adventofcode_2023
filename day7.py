import re
import functools
import heapq
import collections
import enum

LABELS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
LABELS_JOKER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
Kind = enum.Enum(
    "Kind",
    [
        "HIGH_CARD",
        "ONE_PAIR",
        "TWO_PAIR",
        "THREE_OF_A_KIND",
        "FULL_HOUSE",
        "FOUR_OF_A_KIND",
        "FIVE_OF_A_KIND",
    ],
)


@functools.total_ordering
class Hand:
    def __init__(self, cards: str):
        self.cards = cards

    def __repr__(self):
        return f"Hand({self.cards} {self.kind()})"

    def kind(self):
        kind_dict = collections.defaultdict(int)
        for card in self.cards:
            kind_dict[card] = kind_dict[card] + 1

        if max(kind_dict.values()) == 5:
            return Kind.FIVE_OF_A_KIND
        if max(kind_dict.values()) == 4:
            return Kind.FOUR_OF_A_KIND
        if max(kind_dict.values()) == 3 and min(kind_dict.values()) == 2:
            return Kind.FULL_HOUSE
        if max(kind_dict.values()) == 3:
            return Kind.THREE_OF_A_KIND
        if max(kind_dict.values()) == 2 and len(kind_dict.values()) == 3:
            return Kind.TWO_PAIR
        if max(kind_dict.values()) == 2 and len(kind_dict.values()) == 4:
            return Kind.ONE_PAIR
        return Kind.HIGH_CARD

    def _is_valid_operand(self, other):
        return isinstance(other, Hand)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        if self.kind() == other.kind():
            for i in range(0, 5):
                idx = LABELS.index(self.cards[i])
                other_idx = LABELS.index(other.cards[i])
                if idx != other_idx:
                    return idx < other_idx
            return False
        else:
            return self.kind().value < other.kind().value

    def __eq__(self, other):
        return self.cards == other.cards


@functools.total_ordering
class JokerHand:
    def __init__(self, cards: str):
        self.cards = cards

    def __repr__(self):
        return f"JokerHand({self.cards} {self.kind()})"

    def kind(self):
        kind_dict = collections.defaultdict(int)
        joker_count = 0
        for card in self.cards:
            if card == "J":
                joker_count = joker_count + 1
            else:
                kind_dict[card] = kind_dict[card] + 1

        if joker_count == 5:
            return Kind.FIVE_OF_A_KIND
        elif joker_count == 4:
            return Kind.FIVE_OF_A_KIND
        elif joker_count == 3:
            if len(kind_dict) == 1:
                return Kind.FIVE_OF_A_KIND
            else:
                return Kind.FOUR_OF_A_KIND
        elif joker_count == 2:
            if len(kind_dict) == 1:
                return Kind.FIVE_OF_A_KIND
            elif len(kind_dict) == 2:
                return Kind.FOUR_OF_A_KIND
            else:
                return Kind.THREE_OF_A_KIND
        elif joker_count == 1:
            if max(kind_dict.values()) == 4:
                return Kind.FIVE_OF_A_KIND
            elif max(kind_dict.values()) == 3:
                return Kind.FOUR_OF_A_KIND
            elif max(kind_dict.values()) == 2:
                if len(kind_dict) == 2:
                    return Kind.FULL_HOUSE
                else:
                    return Kind.THREE_OF_A_KIND
            else:
                return Kind.ONE_PAIR

        if max(kind_dict.values()) == 5:
            return Kind.FIVE_OF_A_KIND
        if max(kind_dict.values()) == 4:
            return Kind.FOUR_OF_A_KIND
        if max(kind_dict.values()) == 3 and min(kind_dict.values()) == 2:
            return Kind.FULL_HOUSE
        if max(kind_dict.values()) == 3:
            return Kind.THREE_OF_A_KIND
        if max(kind_dict.values()) == 2 and len(kind_dict.values()) == 3:
            return Kind.TWO_PAIR
        if max(kind_dict.values()) == 2 and len(kind_dict.values()) == 4:
            return Kind.ONE_PAIR
        return Kind.HIGH_CARD

    def _is_valid_operand(self, other):
        return isinstance(other, JokerHand)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        if self.kind() == other.kind():
            for i in range(0, 5):
                idx = LABELS_JOKER.index(self.cards[i])
                other_idx = LABELS_JOKER.index(other.cards[i])
                if idx != other_idx:
                    return idx < other_idx
            return False
        else:
            return self.kind().value < other.kind().value

    def __eq__(self, other):
        return self.cards == other.cards


class Solver:
    def __init__(self, file_name):
        self.file_name = file_name

        self.lines = []
        with open(self.file_name, "r", encoding="utf-8") as file:
            for line in file:
                self.lines.append(line.strip())

    def part_one(self):
        hands = []

        for line in self.lines:
            cards, bid = line.split(" ")
            heapq.heappush(hands, (Hand(cards), int(bid)))

        return sum(heapq.heappop(hands)[1] * (i + 1) for i in range(len(hands)))

    def part_two(self):
        hands = []

        for line in self.lines:
            cards, bid = line.split(" ")
            heapq.heappush(hands, (JokerHand(cards), int(bid)))

        # print("\n".join(list(f"{heapq.heappop(hands)[0]}" for i in range(len(hands)))))
        return sum(heapq.heappop(hands)[1] * (i + 1) for i in range(len(hands)))


if __name__ == "__main__":
    example_solver = Solver("data/day7_input_example.txt")
    solver = Solver("data/day7_input.txt")
    print(f"Q1 (Example): {example_solver.part_one()}")
    print(f"Q2 (Example): {example_solver.part_two()}")
    print(f"Q1: {solver.part_one()}")
    print(f"Q2: {solver.part_two()}")
