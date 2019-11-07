from v1.board import Board
from v1.loader import getBoardFromFile


def clearConsole():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def update(): ## Rendering is incorrect, check GUI version to see that moving does work
    clearConsole()
    boardState = board.getBoard()
    line = ""
    for i in range(len(boardState)):
        line += "".join(boardState[i]) + "\n"

    print(line)

board = Board()

board.initBoard(getBoardFromFile("../gamesetups/level2.txt"))
update()

while not board.isGameWon():
    direction = input("Input direction! (l/r/u/d)")
    if direction == "q":
        break
    board.move(direction)
    update()

print("Game finished")
