from utils import get_lines


class Rock:
    points = 1

    @staticmethod
    def win_points(other) -> int:
        if isinstance(other, Rock):
            return 3
        if isinstance(other, Paper):
            return 0
        if isinstance(other, Scissors):
            return 6
        raise ValueError

    @staticmethod
    def wins_against():
        return Scissors()

    @staticmethod
    def looses_against():
        return Paper()


class Paper:
    points = 2

    @staticmethod
    def win_points(other) -> int:
        if isinstance(other, Rock):
            return 6
        if isinstance(other, Paper):
            return 3
        if isinstance(other, Scissors):
            return 0
        raise ValueError

    @staticmethod
    def wins_against():
        return Rock()

    @staticmethod
    def looses_against():
        return Scissors()


class Scissors:
    points = 3

    @staticmethod
    def win_points(other) -> int:
        if isinstance(other, Rock):
            return 0
        if isinstance(other, Paper):
            return 6
        if isinstance(other, Scissors):
            return 3
        raise ValueError

    @staticmethod
    def wins_against():
        return Paper()

    @staticmethod
    def looses_against():
        return Rock()


def rock_paper_scissors_factory(item: str) -> Rock | Paper | Scissors:
    if item in {"A", "X"}:
        return Rock()
    if item in {"B", "Y"}:
        return Paper()
    if item in {"C", "Z"}:
        return Scissors()
    raise ValueError("You did not choose a proper character for Rock, Paper or Scissors")


lines = get_lines("input_day2.txt")

points = 0
for line in lines:
    if line == "":
        continue
    other, mine = line.split(" ")
    other = rock_paper_scissors_factory(other)
    mine = rock_paper_scissors_factory(mine)
    points += mine.points
    points += mine.win_points(other)
print(points)

points = 0
for line in lines:
    if line == "":
        continue
    other, mine = line.split(" ")
    other = rock_paper_scissors_factory(other)
    if mine == "X":
        mine = other.wins_against()
    elif mine == "Y":
        mine = other
    elif mine == "Z":
        mine = other.looses_against()
    else:
        raise ValueError("Should have been X, Y or Z")
    points += mine.points
    points += mine.win_points(other)
print(points)
