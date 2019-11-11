from v2.board import Board


class SolverState(object):
    def __init__(self, previousState, board, actionTuple):
        if previousState is None:
            self.depth = 0
        else:
            self.depth = previousState.depth + 1
        self.board = board
        self.actionTuple = actionTuple


def findSolution(board):
    closedStates = list()
    openStates = list()
    futureStates = list()

    maxDepth = 30

    realisedBoard = Board()
    realisedBoard.initBoardFromStringArray(board)

    finalState = None
    previousState = SolverState(None, realisedBoard, None)
    openStates.append(previousState)

    while finalState is None:
        while len(openStates) > 0:
            currentState = openStates.pop()
            if currentState.board.getHash() not in closedStates:
                actions = currentState.board.getAvailableActions()
                for can, action in actions:
                    workingBoard = currentState.board.replicateBoard()
                    canX = can[0]
                    canY = can[1]
                    playerX, playerY = workingBoard.player.calculatePositionToPerformMove(action, canX, canY)
                    path_to_position = workingBoard.player.pathToPosition(workingBoard, playerX, playerY)
                    if path_to_position is not None:
                        workingBoard.moveCanister(canX, canY, action)
                        workingBoard.player.pathToPosition(workingBoard, canX, canY)
                        if currentState.depth < maxDepth:
                            openStates.append(SolverState(currentState, workingBoard, (can, action)))
                        else:
                            futureStates.append(SolverState(currentState, workingBoard, (can, action)))
            closedStates.append(currentState.board.getHash())



        if finalState is None:
            if len(futureStates) == 0 and len(openStates) == 0:
                print("No solution is possible")
                return

            print("Increasing max depth")
            maxDepth += 1
            for state in futureStates:
                openStates.append(state)
