# File: field.py
# A simple program representing some functions for field in sea battle

import random


def read_file(filename):
    """
    (str) -> (list)
    the function reads the field represented by spaces, * and x for sea battle
    from file
    filename: the name of file or path to it
    return: list of str as lines of field
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read().split("\n")
    return data


def generate_field():
    """
    () -> set
    the function creates the field for sea battle randomly and correctly
    arg: no preconditions
    return: the set of tuples where the coordinates of ship are stored
    """
    f = set()  # represents the set of cells where ship can't be placed
    ship_coord = set()
    ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for sh in ship:
        pos = random.randint(0, 1)  # choose the position for ship

        # horizontal
        if pos:
            col = random.randint(1, 9 - sh)
            row = col

            search = True
            while search:
                # generate coord of cells for this ship
                coord = [(row, col + i - 1) for i in range(sh + 2)]
                search = False
                for el in coord:
                    if el in f:
                        # change the row if the ship can't be placed
                        row = 9 if row == 0 else row - 1

                        # choose another col if there are no place for ship
                        if row == col:
                            col = random.randint(1, 9 - sh)
                            row = col
                        search = True
                        break
                if not search:
                    # add coord for ship and its boards
                    f = f.union(set(coord))
                    f = f.union(
                        set([(row - 1, col + i - 1) for i in range(sh + 2)]))
                    f = f.union(
                        set([(row + 1, col + i - 1) for i in range(sh + 2)]))
                    ship_coord = ship_coord.union(set(coord[1:-1]))

        # vertical
        else:
            row = random.randint(1, 9 - sh)
            col = row

            search = True
            while search:
                # generate coord of cells for this ship
                coord = [(row + i - 1, col) for i in range(sh + 2)]
                search = False
                for el in coord:
                    if el in f:
                        # change the col if the ship can't be placed
                        col = 9 if col == 0 else col - 1

                        # choose another row if there are no place for ship
                        if col == row:
                            row = random.randint(1, 9 - sh)
                            col = row
                        search = True
                        break
                if not search:
                    # add coord for ship and its boards
                    f = f.union(set(coord))
                    f = f.union(
                        set([(row + i - 1, col - 1) for i in range(sh + 2)]))
                    f = f.union(
                        set([(row + i - 1, col + 1) for i in range(sh + 2)]))
                    ship_coord = ship_coord.union(set(coord[1:-1]))

    return ship_coord


def field_to_str(data):
    """
    (list) -> None
    the function write the field represented by list of str for sea battle
    to file
    data: list of str as lines of field
    """
    with open("field.txt", "w") as f:
        for el in data:
            f.write(el + "\n")


def has_ship(data, tup):
    """
    (list, tuple) -> bool
    the function gets the coord of appropriate cell and inform if there is the
    ship in this cell (note: the coord start from 1 while the list index - from
    0)
    :param data: list of str representing field
    :param tup: the coord of cell
    :return: True if there is the ship in the cell
             False otherwise
    """
    row = tup[0]
    col = tup[1]
    if data[row][col] != " ":
        return True
    return False


def ship_size(data, tup):
    """
    (list, tuple) -> tuple
    the function search the size of ship by given cell
    :param data: list of str representing field
    :param tup: the coord of cell
    :return: the tuple by len of the ship vertically and horizontally part of
    which is the given cell
    """
    row = tup[0]
    column = tup[1]

    # looks for len horizontally and vertically
    size_hor = search_ship(data[row], column)
    size_ver = search_ship("".join([data[i][column] for i in range(10)]), row)
    return size_ver, size_hor


def search_ship(line, column):
    """
    (str, int) -> int
    the function looks for the len of ship
    :param line: the str of spaces, x and * that represents ship
    and empty places
    :param column: the index of a part of ship which len should be found
    :return: int as the len of ship
    """
    line = line[:column] + "X" + line[column + 1:]
    ship = line.strip(" ").split(" ")

    if isinstance(ship, str):
        return len(ship)
    for el in ship:
        if "X" in el:
            return len(el)


def is_valid(data):
    """
    (list) -> bool
    the function checks if the given field is valid by location of the ships
    and their amount
    :param data: the list of str representing lines
    :return: True if the field if valid
             False otherwise
    """
    ships = 4 * [4] + 2 * 3 * [3] + 3 * 2 * [2] + 4 * [1]
    field = transform_to_tuple(data)
    for cell in field:
        try:
            if cell[0] == 1 and cell[1] in [1, 2, 3, 4]:
                ships.remove(cell[1])
            elif cell[1] == 1 and cell[0] in [1, 2, 3, 4]:
                ships.remove(cell[0])
            else:
                return False

        except ValueError:
            return False

    return True


def transform_to_tuple(data):
    """
    (list) -> list
    the function looks on every cell and checks if there are some ships on
    diagonals and add info about its vertical and horizontal size of a ship
    :param data: the list of str represents lines
    :return: the list of tuples with info about size
    """
    field = []
    for i in range(10):
        for j in range(10):
            if has_ship(data, (i, j)):

                # look if there is a ship on 4 sides on diagonals
                # if yes, add inappropriate info that later will be detected
                if search_diag(data, i, j):
                    field.append((5, 5))

                # if diag are clear, add info about hor and vert size
                else:
                    field.append(ship_size(data, (i, j)))

    return field


def search_diag(data, i, j):
    """
    (list, int, int) -> bool
    he function looks on cells on diagonals and checks if there some ships on
    them
    :param data: the list of str represents lines
    :param i: row
    :param j: col
    :return: True if there is a ship on diagonals
             False otherwise
    """
    if i >= 1:
        if j >= 1:
            if has_ship(data, (i - 1, j - 1)):
                return True
        elif j <= 8:
            if has_ship(data, (i - 1, j + 1)):
                return True
    elif i <= 8:
        if j >= 1:
            if has_ship(data, (i + 1, j - 1)):
                return True
        elif j <= 8:
            if has_ship(data, (i + 1, j + 1)):
                return True
    return False


def transform(field):
    return ["".join(["*" if (i,j) in field
                     else " " for j in range(10)]) for i in range(10)]


if __name__ == "__main__":
    field1 = transform(generate_field())
    print("We generate random field. "
          "The field is {}".format("valid" if is_valid(field1) else "invalid"))
    print("\n".join(field1))

    field2 = read_file("field2.txt")
    print("We read the field from file 'field2.txt'. "
          "The field is {}".format("valid" if is_valid(field2) else "invalid"))
    print("\n".join(field2))
