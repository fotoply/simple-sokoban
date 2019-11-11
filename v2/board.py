import copy
import enum
from typing import List

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
                    row[len(row)-1].setPlayer(True)
                    self.player = Player(x, y)
                elif stringCell == CANISTER_CHARACTER or stringCell == CANISTER_ON_OBJECTIVE_CHARACTER:
                    if stringCell == CANISTER_ON_OBJECTIVE_CHARACTER:
                        row.append(Cell(CellTypes.objective))
                    else:
                        row.append(Cell(CellTypes.empty))
                    row[len(row)-1].setCanister(True)
                    can = Canister(x, y)
                    self.canisters.append(can)
                else:
                    row.append(Cell(CellTypes.empty))
            self.board.append(row)

    def getAvailableActions(self):
        actions = {}
        for can in self.canisters:
            position = (can.x, can.y)
            actions[position] = can.getPossibleMoves(self.getSurroundings(can.x, can.y))
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
        newBoard.board = copy.copy(self.board)
        newBoard.canisters = copy.deepcopy(self.canisters)
        newBoard.player = copy.deepcopy(self.player)
        return newBoard

    def getEdgeCell(self):
        return Cell(CellTypes.wall)

    def getSurroundings(self, x, y):
        surroundings = list()
        surroundings.append(self.getCell(x + 1, y))
        surroundings.append(self.getCell(x - 1, y))
        surroundings.append(self.getCell(x, y + 1))
        surroundings.append(self.getCell(x, y - 1))
        return surroundings

    def moveCanister(self, x, y, direction):
        can = self.getCanister(x, y)
        can.move(direction)

        self.clearCell(x, y)
        newCell = Cell(self.getCell(can.x, can.y).cellType)
        newCell.setCanister(True)
        self.setCell(can.x, can.y, newCell)


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


class Player(MoveableObject):
    def calculatePositionToPerformMove(self, direction, x, y):
        if direction == UP_MOVE:
            return x, y + 1
        elif direction == RIGHT_MOVE:
            return x - 1, y
        elif direction == DOWN_MOVE:
            return x, y - 1
        elif direction == LEFT_MOVE:
            return x + 1, y

    def pathToPosition(self, board: List[List[Cell]], x, y):
        pass


class Canister(MoveableObject):

    def getPossibleMoves(self, surroundings: List[Cell]):
        moves = list()
        if surroundings[0].isPassable() and surroundings[2].isWalkable():
            moves.append(UP_MOVE)

        if surroundings[1].isPassable() and surroundings[3].isWalkable():
            moves.append(RIGHT_MOVE)

        if surroundings[2].isPassable() and surroundings[0].isWalkable():
            moves.append(DOWN_MOVE)

        if surroundings[3].isPassable() and surroundings[1].isWalkable():
            moves.append(LEFT_MOVE)

        return moves
