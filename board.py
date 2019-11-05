import copy


class Board:
    import copy

    ## Board data structure ##
    ##   = empty space
    ## # = wall space
    ## p = player token (see moveable table)
    ## P = player on target
    ## m = moveable token (see moveable table)
    ## M = moveable on target
    ## o = end space
    ##########################
    board = []
    moveables = []
    playerX = 0
    playerY = 0
    moveCount = 0
    totalMarks = 0
    totalMoveables = 0

    def getBoard(self):
        localBoard = copy.deepcopy(self.board)
        for moveable in self.moveables:
            if localBoard[moveable[0]][moveable[1]] == "o":
                localBoard[moveable[0]][moveable[1]] = "M"
            else:
                localBoard[moveable[0]][moveable[1]] = "m"
        if localBoard[self.playerX][self.playerY] == "o":
            localBoard[self.playerX][self.playerY] = "P"
        else:
            localBoard[self.playerX][self.playerY] = "p"
        return localBoard

    def isGameWon(self):
        for moveable in self.moveables:
            if self.board[moveable[0]][moveable[1]] != "o":
                return False
        return True

    def getMoveCount(self):
        return self.moveCount

    def initBoard(self, newBoard):
        self.moveCount = 0
        self.board = copy.deepcopy(newBoard)
        self.moveables = list()
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == "p":
                    self.playerX = x
                    self.playerY = y
                    self.board[x][y] = "_"
                elif self.board[x][y] == "P":
                    self.totalMarks += 1
                    self.playerX = x
                    self.playerY = y
                    self.board[x][y] = "o"
                elif self.board[x][y] == "m":
                    self.totalMoveables += 1
                    self.board[x][y] = "_"
                    self.moveables.append((x, y))
                elif self.board[x][y] == "M":
                    self.totalMoveables +=1
                    self.totalMarks +=1
                    self.board[x][y] = "o"
                    self.moveables.append((x, y))
                elif self.board[x][y] == "o":
                    self.totalMarks += 1
        if self.totalMarks != self.totalMoveables:
            print("something went wrong")

    def getSpaceType(self, x, y):
        return self.board[x][y]

    def isSpaceAvailable(self, x, y):
        if x < 0 or y < 0:
            return False
        if self.board[x][y] == "_" or self.board[x][y] == "o":
            return True
        if self.board[x][y] == "#":
            return False
        return True

    def canMoveableMoveInDirection(self, x, y, direction):
        if direction == "r" or direction == "right":
            if self.isSpaceAvailable(x + 1, y) and not (x + 1, y) in self.moveables:
                return True
        elif direction == "l" or direction == "left":
            if self.isSpaceAvailable(x - 1, y) and not (x - 1, y) in self.moveables:
                return True
        elif direction == "d" or direction == "down":
            if self.isSpaceAvailable(x, y + 1) and not (x, y + 1) in self.moveables:
                return True
        elif direction == "u" or direction == "up":
            if self.isSpaceAvailable(x, y - 1) and not (x, y - 1) in self.moveables:
                return True
        return False

    def isMoveable(self, x, y):
        if (x, y) in self.moveables:
            return True
        else:
            return False

    ## Directions = (l)eft, (r)ight, (u)p, (d)own
    def move(self, direction):
        x = self.playerX
        y = self.playerY
        direction = direction.lower()
        if direction == "r" or direction == "right":
            if self.isSpaceAvailable(x + 1, y):
                if self.isMoveable(x + 1, y):
                    if self.canMoveableMoveInDirection(x + 1, y, direction):
                        index = self.moveables.index((x + 1, y))
                        self.moveables[index] = (x + 2, y)
                        self.playerX += 1
                        self.moveCount += 1

                else:
                    self.playerX += 1
                    self.moveCount += 1

        elif direction == "l" or direction == "left":
            if self.isSpaceAvailable(x - 1, y):
                if self.isMoveable(x - 1, y):
                    if self.canMoveableMoveInDirection(x - 1, y, direction):
                        index = self.moveables.index((x - 1, y))
                        self.moveables[index] = (x - 2, y)
                        self.playerX -= 1
                        self.moveCount += 1

                else:
                    self.playerX -= 1
                    self.moveCount += 1

        elif direction == "d" or direction == "down":
            if self.isSpaceAvailable(x, y + 1):
                if self.isMoveable(x, y + 1):
                    if self.canMoveableMoveInDirection(x, y + 1, direction):
                        index = self.moveables.index((x, y + 1))
                        self.moveables[index] = (x, y + 2)
                        self.playerY += 1
                        self.moveCount += 1

                else:
                    self.playerY += 1
                    self.moveCount += 1

        elif direction == "u" or direction == "up":
            if self.isSpaceAvailable(x, y - 1):
                if self.isMoveable(x, y - 1):
                    if self.canMoveableMoveInDirection(x, y - 1, direction):
                        index = self.moveables.index((x, y - 1))
                        self.moveables[index] = (x, y - 2)
                        self.playerY -= 1
                        self.moveCount += 1

                else:
                    self.playerY -= 1
                    self.moveCount += 1

        # output.update()
