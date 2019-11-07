import PySimpleGUI as sg
from v1.board import  Board
from v1.loader import getBoardFromFile

layout = [[sg.Canvas(size=(500, 500), background_color='red', key= 'canvas')]]
window = sg.Window('Sokoban', return_keyboard_events=True, layout=layout)
window.finalize()

#initBoard([["#", "#", "#", "#", "#", "#"],
#           ["#", "_", "_", "_", "_", "#"],
#           ["#", "_", "p", "m", "o", "#"],
#           ["#", "_", "m", "_", "_", "#"],
#           ["#", "_", "o", "_", "_", "#"],
#           ["#", "#", "#", "#", "#", "#"]])

board = Board()

board.initBoard(getBoardFromFile("../gamesetups/level3.txt"))

canvas = window.Element('canvas')


def getHash(state):
    playerHash = ""
    moveableHash = ""
    for y in range(len(state)):
        for x in range(len(state[y])):
            cell = state[y][x]
            if cell == "p" or cell == "P":
                playerHash = str(y).zfill(2) + str(x).zfill(2)
            elif cell == "m" or cell == "M":
                moveableHash += str(y).zfill(2) + str(x).zfill(2)
    return playerHash + moveableHash

def drawBoard():
    global board
    canvas.TKCanvas.delete("all")
    boardState = board.getBoard()
    for x in range(len(boardState)):
        for y in range(len(boardState[x])):
            space = boardState[x][y]
            visualX = x*20
            visualY = y*20
            if space == "#":
                canvas.TKCanvas.create_rectangle(visualX, visualY, visualX+20, visualY+20, fill="blue")
            elif space == "o":
                canvas.TKCanvas.create_oval(visualX, visualY, visualX+20, visualY+20, fill="green")
            elif space == "p":
                canvas.TKCanvas.create_oval(visualX+5, visualY, visualX + 10, visualY + 20, fill="blue")
            elif space == "m":
                canvas.TKCanvas.create_rectangle(visualX+5, visualY, visualX + 10, visualY + 20, fill="green")
drawBoard()


while True:
    event, values = window.Read()
    if event is not None:
        inputValue = event.split(":")[0]
        print(inputValue)
        if inputValue == "p":
            print(getHash(board.getBoard()))
        board.move(inputValue)
        drawBoard()
        if board.isGameWon():
            break
    else:
        break
print("Game completed")

window.Close()