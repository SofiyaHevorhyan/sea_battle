# File: sea_battle.py
# A simple program for sea battle

from battlefield import Game

game = Game()
player = 0
current_player = game.players[player]

print("Game Battleship")

end = False

while not end:

    print("\n")
    print("Field of {} player:".format(["second", "first"][player]))
    print(game.field[player-1].field_without_ship())

    pos = game.players[player].read_position()
    try:
        switch = True
        if pos[0] in "ABCDEFGHIJ" and pos[1] in "12345678910":
            game.field[player-1].shoot_at(pos)
        elif pos == "end":
            end = True
        elif pos == "hint":
            print(game.field[player-1].field_with_ship())
        else:
            print("Sorry, we didn't get it. Try again")
            switch = False
    except IndexError:
        switch = False

    if switch:
        player = 0 if player else 1
