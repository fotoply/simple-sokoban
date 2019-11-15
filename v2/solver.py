import time

from v2.board import Board


class SolverState(object):
    def __init__(self, previousState, board, actionTuple, playerMoves):
        if previousState is None:
            self.depth = 0 + len(playerMoves)
            self.previousState = None
        else:
            self.depth = previousState.depth + 1 + len(playerMoves)
            self.previousState = previousState
        self.board = board
        self.actionTuple = actionTuple
        self.playerMoves = playerMoves


def findSolution(board, robotMode=False, heading="u"):
    closedStates = set()
    openStates = list()
    futureStates = list()

    maxDepth = 1

    realisedBoard = Board()
    realisedBoard.initBoardFromStringArray(board)

    finalState = None
    previousState = SolverState(None, realisedBoard, None, list())
    openStates.append(previousState)

    while finalState is None:
        while len(openStates) > 0:
            finalState = processState(closedStates, finalState, futureStates, maxDepth, openStates, openStates.pop())

        if finalState is None:
            if len(futureStates) == 0 and len(openStates) == 0:
                print("No solution is possible")
                return

            print("Increasing max depth (" + str(maxDepth + 1) + ")" + " / Closed states: " + str(len(closedStates)))
            maxDepth += 1
            openStates.extend(futureStates)
            futureStates.clear()
        else:
            print("Total states explored: " + str(len(closedStates)))
            state = finalState

            if not robotMode:
                finalPath = list()
                while state.previousState is not None:
                    finalPath.append(state.actionTuple[1])
                    state.playerMoves.reverse()
                    finalPath.extend(state.playerMoves)
                    state = state.previousState

                finalPath.reverse()
                string = ""
                for s in finalPath:
                    string += s
                return string
            else:
                finalPath = ""
                statePath = list()
                statePath.append(finalState)
                while state.previousState is not None:
                    statePath.append(state.previousState)
                    state = state.previousState
                statePath.reverse()

                localHeading = heading
                for state in statePath:
                    if state.actionTuple is not None:
                        for move in state.playerMoves:
                            forwardsMove = "f"
                            extraPath, localHeading = parseMove(forwardsMove, localHeading, move)
                            finalPath += extraPath
                        extraPath, localHeading = parseMove("fo", localHeading, state.actionTuple[1])
                        finalPath += extraPath
                return finalPath


def parseMove(forwardsMove, rotation, move):
    if move == rotation:
        return forwardsMove, rotation
    else:
        if isOpposites(move, rotation):
            path = "u" + forwardsMove
            rotation = getOpposite(rotation)
            return path, rotation
        else:
            rotation = getRotationDirection(move, rotation)
            path = rotation + forwardsMove
            return path, move


def getRotationDirection(move, heading):
    if move == "r":
        if heading == "u":
            return "r"
        elif heading == "d":
            return "l"
    if move == "l":
        if heading == "u":
            return "l"
        elif heading == "d":
            return "r"
    if move == "u":
        if heading == "l":
            return "r"
        elif heading == "r":
            return "l"
    if move == "d":
        if heading == "l":
            return "l"
        elif heading == "r":
            return "r"


def isOpposites(move, heading):
    if getOpposite(move) == heading:
        return True
    return False

def getOpposite(heading):
    if heading == "r":
        return "l"
    if heading == "l":
        return "r"
    if heading == "u":
        return "d"
    if heading == "d":
        return "u"



def processState(closedStates, finalState, futureStates, maxDepth, openStates, currentState):
    if currentState.board.getHash() not in closedStates:
        if currentState.board.isWinable():
            allActions = currentState.board.getAvailableActions()
            for canX, canY in allActions:
                canActions = allActions[canX, canY]
                for action in canActions:
                    workingBoard = currentState.board.replicateBoard()
                    playerX, playerY = workingBoard.player.calculatePositionToPerformMove(action, canX, canY)
                    path_to_position = workingBoard.player.pathToPosition(workingBoard, playerX, playerY)
                    if path_to_position is not None:
                        workingBoard.moveCanister(canX, canY, action)
                        pushCan = workingBoard.player.pathToPosition(workingBoard, canX, canY)
                        workingState = SolverState(currentState, workingBoard, ((canX, canY), action), path_to_position)
                        #workingState.board.print()
                        if workingBoard.isWon():
                            if finalState is None:
                                finalState = workingState
                            else:
                                if finalState.depth > workingState.depth:
                                    finalState = workingState

                        if workingState.board.isWinable():
                            if currentState.depth < maxDepth:
                                openStates.append(workingState)
                            else:
                                futureStates.append(workingState)
                        else:
                            closedStates.add(workingState.board.getHash())
        closedStates.add(currentState.board.getHash())
    return finalState


if __name__ == "__main__":
    from v2.loader import getBoardFromFile

    beforeTime = time.time()
    solution = findSolution(getBoardFromFile("../gamesetups/MMMILevel.txt"), robotMode=True)
    print("Solution:")
    print(solution)
    print("Time taken:" + str(time.time() - beforeTime))
