from board import move, getBoard, initBoard, isGameWon


def clearConsole():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def update(): ## Rendering is incorrect, check GUI version to see that moving does work
    clearConsole()
    board = getBoard()
    line = ""
    for i in range(len(board)):
        line += "".join(board[i]) + "\n"

    print(line)

initBoard([["#", "#", "#", "#", "#", "#"],
           ["#", "_", "_", "_", "_", "#"],
           ["#", "_", "p", "m", "o", "#"],
           ["#", "_", "m", "_", "_", "#"],
           ["#", "_", "o", "_", "_", "#"],
           ["#", "#", "#", "#", "#", "#"]])
update()

while not isGameWon():
    direction = input("Input direction! (l/r/u/d)")
    if direction == "q":
        break
    move(direction)
    update()

print("Game finished")
