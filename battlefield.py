# File: battlefield.py
# A simple program representing some classes and functions for sea battle

import field


class Game:
    """
    Represents a game sea battle - with players and fields
    """
    def __init__(self):
        """
        Initialize fields and players
        """
        self.field = [Field(), Field()]
        self.players = [Player("Player 1"), Player("Player 2")]


class Field:
    """
    Represents a field with ships
    """
    def __init__(self):
        """
        Initialize the field with ships
        """
        self.field = self.create_field()

    def create_field(self):
        """
        Creates a random field and return the list of lists where every el is
        Ship obj
        :return: the list of lists
        """
        ship_coord = field.generate_field()
        return [[Ship(1) if (i, j) in ship_coord
                 else Ship(0) for j in range(10)] for i in range(10)]

    def shoot_at(self, tup):
        row = ord(tup[0].upper()) - 65
        col = int(tup[1]) - 1
        if self.field[row][col].ship:
            self.field[row][col].hit = True

    def field_with_ship(self):
        field = ["".join(["x" if cell.ship and cell.hit else
                          "*" if cell.ship else
                          " " for cell in row]) for row in self.field]
        return "\n".join(field)

    def field_without_ship(self):
        field = ["".join(["x" if cell.hit else " " for cell in row]) for row in self.field]
        return "\n".join(field)


class Player:
    def __init__(self, name):
        self.name = name

    def read_position(self):
        pos = input("{}, enter move: ".format(self.name))
        return pos


class Ship:
    """
    Represents a cell on field
    """
    def __init__(self, presence):
        """
        Initialize the cell with info about whether there is a ship in a cell
        param hit represents if the ship in the cell is hit. True if yes, False
        is no, None if there is no ship in the cell
        :param presence: int
        """
        self.ship = True if presence else False
        self.hit = False if presence else None


if __name__ == "__main__":
    game = Game()
    pos = game.players[0].read_position()
    game.field[0].shoot_at(pos)
    print(game.field[0].field_without_ship())
    print(game.field[0].field_with_ship())
