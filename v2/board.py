import copy
import enum
import math
from typing import List, Tuple

WALL_CHARACTER = "#"
PLAYER_CHARACTER = "p"
PLAYER_ON_OBJECTIVE_CHARACTER = "P"
OBJECTIVE_CHARACTER = "o"
OPEN_SPACE_CHARACTER = " "
CANISTER_CHARACTER = "m"
CANISTER_ON_OBJECTIVE_CHARACTER = "M"

UP_MOVE = "u"
RIGHT_MOVE = "r"
DOWN_MOVE = "d"
LEFT_MOVE = "l"


class CellTypes(enum.Enum):
    wall = WALL_CHARACTER
    empty = OPEN_SPACE_CHARACTER
    objective = OBJECTIVE_CHARACTER


class Cell:
    def __init__(self, cellType: CellTypes):
        self.cellType = cellType
        self.player = False
        self.canister = False

    def __str__(self):
        return self.cellType

    def duplicate(self):
        newCell = Cell(self.cellType)
        newCell.player = self.player
        newCell.canister = self.canister
        return newCell

    def setPlayer(self, playerBool: bool):
        self.player = playerBool

    def hasPlayer(self):
        return self.player

    def setCanister(self, canisterBool: bool):
        self.canister = canisterBool

    def hasCanister(self):
        return self.canister

    def isPassable(self):
        if self.hasPlayer():
            return False
        return self.isWalkable()

    def isWalkable(self):
        if self.cellType == CellTypes.wall or self.hasCanister():
            return False
        else:
            return True


class Board:
    ###
    # board is a 2 dimensional array of the shape (y,x), eg. [[ROW],[ROW],etc]
    ###
    def __init__(self):
        self.canisters = list()  ## A list of Cell objects
        self.board = list()

    def initBoardFromStringArray(self, board):
        for y in range(len(board)):
            row = list()
            for x in range(len(board[y])):
                stringCell = board[y][x]
                if stringCell == WALL_CHARACTER:
                    row.append(Cell(CellTypes.wall))
                elif stringCell == OBJECTIVE_CHARACTER:
                    row.append(Cell(CellTypes.objective))
                elif stringCell == PLAYER_CHARACTER or stringCell == PLAYER_ON_OBJECTIVE_CHARACTER:
                    if stringCell == PLAYER_ON_OBJECTIVE_CHARACTER:
                        row.append(Cell(CellTypes.objective))
                    else:
                        row.append(Cell(CellTypes.empty))
                    row[len(row) - 1].setPlayer(True)
                    self.player = Player(x, y)
                elif stringCell == CANISTER_CHARACTER or stringCell == CANISTER_ON_OBJECTIVE_CHARACTER:
                    if stringCell == CANISTER_ON_OBJECTIVE_CHARACTER:
                        row.append(Cell(CellTypes.objective))
                    else:
                        row.append(Cell(CellTypes.empty))
                    row[len(row) - 1].setCanister(True)
                    can = Canister(x, y)
                    self.canisters.append(can)
                else:
                    row.append(Cell(CellTypes.empty))
            self.board.append(row)

    def getAvailableActions(self):
        actions = {}
        for can in self.canisters:
            position = (can.x, can.y)
            actions[position] = can.getAvailableMoves(self.getSurroundings(can.x, can.y))
        return actions

    def getHash(self):
        self.canisters.sort(key=lambda x: (x.x, x.y))
        canisterHash = ""
        for can in self.canisters:
            canisterHash += can.getHash()
        return self.player.getHash() + canisterHash

    def initPlayer(self, player):
        self.player = player
        newCell = self.getCell(player.x, player.y).duplicate()
        newCell.setPlayer(True)
        self.setCell(player.x, player.y, newCell)

    def isWon(self):
        for canister in self.canisters:
            if self.getCell(canister.x, canister.y).cellType != CellTypes.objective:
                return False

        return True

    def isWinable(self):
        for can in self.canisters:
            if can.isCornered(self.getSurroundings(can.x, can.y)) and self.getCell(can.x, can.y).cellType != CellTypes.objective:
                return False
        return True

    def getCanister(self, x, y):
        for can in self.canisters:
            if can.x == x and can.y == y:
                return can
        return None

    def getCell(self, x, y) -> Cell:
        if y > len(self.board) - 1 or y < 0:
            return self.getEdgeCell()
        if x > len(self.board[y]) or x < 0:
            return self.getEdgeCell()
        return self.board[y][x]

    def clearCell(self, x, y):
        self.setCell(x, y, Cell(CellTypes.empty))

    def setCell(self, x, y, cell: Cell):
        self.board[y][x] = cell

    def replicateBoard(self):
        newBoard = Board()
        newBoard.board = list()
        for row in self.board:
            newBoard.board.append(copy.copy(row))
        newBoard.canisters = list()
        for can in self.canisters:
            newBoard.canisters.append(can.duplicate())
        newBoard.player = self.player.duplicate()
        return newBoard

    def getEdgeCell(self):
        return Cell(CellTypes.wall)

    def getSurroundings(self, x, y):
        surroundings = list()
        surroundings.append(self.getCell(x, y - 1))
        surroundings.append(self.getCell(x + 1, y))
        surroundings.append(self.getCell(x, y + 1))
        surroundings.append(self.getCell(x - 1, y))
        return surroundings

    def moveCanister(self, x, y, direction):
        can = self.getCanister(x, y)
        can.move(direction)

        self.clearCell(x, y)
        newCell = self.getCell(can.x, can.y).duplicate()
        newCell.setCanister(True)
        self.setCell(can.x, can.y, newCell)

    def print(self):
        for row in self.board:
            rowString = ""
            for cell in row:
                if cell.hasPlayer():
                    rowString += PLAYER_CHARACTER
                elif cell.hasCanister():
                    rowString += CANISTER_CHARACTER
                else:
                    rowString += cell.cellType.value
            print(rowString)


class MoveableObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.previousX = x
        self.previousY = y

    def move(self, direction):
        self.previousX = self.x
        self.previousY = self.y

        if direction == UP_MOVE:
            self.y -= 1
        elif direction == RIGHT_MOVE:
            self.x += 1
        elif direction == DOWN_MOVE:
            self.y += 1
        elif direction == LEFT_MOVE:
            self.x -= 1

    def getPosition(self):
        return self.x, self.y

    def getPreviousPosition(self):
        return self.previousX, self.previousY

    def getHash(self):
        return str(self.x).zfill(2) + str(self.y).zfill(2)


class PathState:
    def __init__(self, x, y, previous, move):
        self.x = x
        self.y = y
        if previous is None:
            self.depth = 0
            self.previous = None
        else:
            self.previous = previous
            self.depth = previous.depth + 1
        self.move = move

    def getPos(self):
        return self.x, self.y


class Player(MoveableObject):
    def duplicate(self):
        newPlayer = Player(self.x, self.y)
        newPlayer.previousX = self.previousX
        newPlayer.previousY = self.previousY
        return newPlayer

    def calculatePositionToPerformMove(self, direction, x, y):
        if direction == UP_MOVE:
            return x, y + 1
        elif direction == RIGHT_MOVE:
            return x - 1, y
        elif direction == DOWN_MOVE:
            return x, y - 1
        elif direction == LEFT_MOVE:
            return x + 1, y

    def getAvailableMoves(self, surroundings: List[Cell]):
        moves = list()
        if surroundings[0].isWalkable():
            moves.append(UP_MOVE)

        if surroundings[1].isWalkable():
            moves.append(RIGHT_MOVE)

        if surroundings[2].isWalkable():
            moves.append(DOWN_MOVE)

        if surroundings[3].isWalkable():
            moves.append(LEFT_MOVE)
        return moves

    def distanceToPoint(self, start: Tuple, end: Tuple):
        return (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2

    def getPositionAfterMove(self, x, y, direction):
        if direction == UP_MOVE:
            return x, y - 1
        if direction == DOWN_MOVE:
            return x, y + 1
        if direction == RIGHT_MOVE:
            return x + 1, y
        if direction == LEFT_MOVE:
            return x - 1, y

    def pathToPosition(self, board: Board, x, y):
        openSet = list()
        closedSet = list()
        finalState = None
        initialState = PathState(self.x, self.y, None, None)
        openSet.append(initialState)

        if self.x == x and self.y == y:
            finalState = initialState

        while len(openSet) > 0 and finalState is None:
            openSet.sort(key=lambda val: self.distanceToPoint(val.getPos(), (x, y)) + val.depth, reverse=True)
            localState = openSet.pop()
            localX = localState.x
            localY = localState.y
            moves = self.getAvailableMoves(board.getSurroundings(localX, localY))
            for move in moves:
                moveX, moveY = self.getPositionAfterMove(localX, localY, move)
                if (moveX, moveY) not in closedSet:
                    newState = PathState(moveX, moveY, localState, move)
                    openSet.append(newState)
                    if moveX == x and moveY == y:
                        finalState = newState

            closedSet.append((localX, localY))

        if finalState is None:
            return None
        else:
            self.previousX = self.x
            self.previousY = self.y
            self.x = x
            self.y = y
            board.clearCell(board.player.previousX, board.player.previousY)
            newCell = board.getCell(x, y).duplicate()
            newCell.setPlayer(True)
            board.setCell(x, y, newCell)
            path = list()
            previousState = finalState
            while previousState.previous is not None:
                path.append(previousState.move)
                previousState = previousState.previous

            path.reverse()
            return path


class Canister(MoveableObject):

    def getAvailableMoves(self, surroundings: List[Cell]):
        moves = list()
        if surroundings[0].isWalkable() and surroundings[2].isWalkable():
            moves.append(UP_MOVE)

        if surroundings[1].isWalkable() and surroundings[3].isWalkable():
            moves.append(RIGHT_MOVE)

        if surroundings[2].isWalkable() and surroundings[0].isWalkable():
            moves.append(DOWN_MOVE)

        if surroundings[3].isWalkable() and surroundings[1].isWalkable():
            moves.append(LEFT_MOVE)

        return moves

    def duplicate(self):
        can = Canister(self.x, self.y)
        can.previousX = self.previousX
        can.previousY = self.previousY
        return can

    def isCornered(self, surroundings):
        if surroundings[0].cellType == CellTypes.wall and surroundings[1].cellType == CellTypes.wall:
            return True
        if surroundings[1].cellType == CellTypes.wall and surroundings[2].cellType == CellTypes.wall:
            return True
        if surroundings[2].cellType == CellTypes.wall and surroundings[3].cellType == CellTypes.wall:
            return True
        if surroundings[3].cellType == CellTypes.wall and surroundings[0].cellType == CellTypes.wall:
            return True
        return False