import copy

output = None

## Board data structure ##
## _ = empty space
## # = wall space
## p = player token (see moveable table)
## m = moveable token (see moveable table)
## o = end space
##########################
board = []
moveables = []
playerX = 0
playerY = 0
moveCount = 0


def getBoard():
    global board, moveables
    localBoard = copy.deepcopy(board)
    for moveable in moveables:
        localBoard[moveable[0]][moveable[1]] = "m"
    localBoard[playerX][playerY] = "p"
    return localBoard

def isGameWon():
    for moveable in moveables:
        if board[moveable[0]][moveable[1]] != "o":
            return False
    return True

def getMoveCount():
    global moveCount
    return moveCount


def initBoard(newBoard):
    global board, moveables
    board = newBoard.copy()
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == "p":
                global playerY, playerX
                playerX = x
                playerY = y
                board[x][y] = "_"
            elif board[x][y] == "m":
                board[x][y] = "_"
                moveables.append((x, y))


def registerOutput(outputStream): ## Doesn't work atm
    global output
    output = outputStream


def getSpaceType(x, y):
    global board
    return board[x][y]


def isSpaceAvailable(x, y):
    global board
    if board[x][y] == "_" or board[x][y] == "o":
        return True
    if board[x][y] == "#":
        return False


def canMoveableMoveInDirection(x, y, direction):
    global moveables
    if direction == "r" or direction == "right":
        if isSpaceAvailable(x + 1, y) and not (x + 1, y) in moveables:
            return True
    elif direction == "l" or direction == "left":
        if isSpaceAvailable(x - 1, y) and not (x - 1, y) in moveables:
            return True
    elif direction == "d" or direction == "down":
        if isSpaceAvailable(x, y + 1) and not (x, y + 1) in moveables:
            return True
    elif direction == "u" or direction == "up":
        if isSpaceAvailable(x, y - 1) and not (x, y - 1) in moveables:
            return True
    return False


def isMoveable(x, y):
    if (x, y) in moveables:
        return True
    else:
        return False


## Directions = (l)eft, (r)ight, (u)p, (d)own
def move(direction):
    global output, moveables, playerY, playerX, moveCount
    x = playerX
    y = playerY
    direction = direction.lower()
    if direction == "r" or direction == "right":
        if isSpaceAvailable(x + 1, y):
            if isMoveable(x + 1, y):
                if canMoveableMoveInDirection(x + 1, y, direction):
                    index = moveables.index((x + 1, y))
                    moveables[index] = (x + 2, y)
                    playerX += 1
                    moveCount += 1

            else:
                playerX += 1
                moveCount += 1

    elif direction == "l" or direction == "left":
        if isSpaceAvailable(x - 1, y):
            if isMoveable(x - 1, y):
                if canMoveableMoveInDirection(x - 1, y, direction):
                    index = moveables.index((x - 1, y))
                    moveables[index] = (x - 2, y)
                    playerX -= 1
                    moveCount += 1

            else:
                playerX -= 1
                moveCount += 1

    elif direction == "d" or direction == "down":
        if isSpaceAvailable(x, y + 1):
            if isMoveable(x, y + 1):
                if canMoveableMoveInDirection(x, y + 1, direction):
                    index = moveables.index((x, y + 1))
                    moveables[index] = (x, y + 2)
                    playerY += 1
                    moveCount += 1

            else:
                playerY += 1
                moveCount += 1

    elif direction == "u" or direction == "up":
        if isSpaceAvailable(x, y - 1):
            if isMoveable(x, y - 1):
                if canMoveableMoveInDirection(x, y - 1, direction):
                    index = moveables.index((x, y - 1))
                    moveables[index] = (x, y - 2)
                    playerY -= 1
                    moveCount += 1

            else:
                playerY -= 1
                moveCount += 1

    #output.update()

