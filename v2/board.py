import copy
import enum
from typing import List

WALL_CHARACTER = "#"
PLAYER_CHARACTER = "p"
PLAYER_ON_OBJECTIVE_CHARACTER = "P"
OBJECTIVE_CHARACTER = "o"
OPEN_SPACE_CHARACTER = " "
CANISTER_CHARACTER = "n"
CANISTER_ON_OBJECTIVE_CHARACTER = "N"

UP_MOVE = "u"
RIGHT_MOVE = "r"
DOWN_MOVE = "d"
LEFT_MOVE = "l"


class Board:
    ###
    # board is a 2 dimensional array of the shape (y,x), eg. [[ROW],[ROW],etc]
    ###
    def __init__(self):
        self.canisters = list() ## A list of Cell objects

    def initBoard(self, board):
        pass

    def isWon(self):
        pass

    def replicateBoard(self):
        newBoard = Board()
        newBoard.board = self.board
        newBoard.canisters = copy.deepcopy(self.canisters)
        newBoard.player = copy.deepcopy(self.player)
        return newBoard

    def getEdgeCell(self):
        return Cell(CellTypes.wall)


class CellTypes(enum.Enum):
    wall = WALL_CHARACTER
    empty = OPEN_SPACE_CHARACTER
    objective = OBJECTIVE_CHARACTER


class Cell:
    def __init__(self, cellType: CellTypes):
        self.cellType = cellType

    def hasPlayer(self):
        pass

    def hasCanister(self):
        pass

    def isPassable(self):
        if self.hasPlayer():
            return False
        return self.hasStaticObject()

    def hasStaticObject(self):
        if self.cellType == CellTypes.wall or self.hasCanister():
            return False
        else:
            return True


class MoveableObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == UP_MOVE:
            self.y -= 1
        elif direction == RIGHT_MOVE:
            self.x += 1
        elif direction == DOWN_MOVE:
            self.y += 1
        elif direction == LEFT_MOVE:
            self.x -= 1


class Player(MoveableObject):
    def pathToPosition(self, board, x, y):
        pass


class Canister(MoveableObject):

    def getHash(self):
        return str(self.x).zfill(2) + str(self.y).zfill(2)

    def getPossibleMoves(self, surroundings: List[Cell]):
        moves = list()
        if surroundings[0].isPassable() and not surroundings[2].hasStaticObject():
            moves.append(UP_MOVE)

        if surroundings[1].isPassable() and not surroundings[3].hasStaticObject():
            moves.append(RIGHT_MOVE)

        if surroundings[2].isPassable() and not surroundings[0].hasStaticObject():
            moves.append(DOWN_MOVE)

        if surroundings[3].isPassable() and not surroundings[1].hasStaticObject():
            moves.append(LEFT_MOVE)

        return moves
