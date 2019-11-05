from board import Board
from loader import getBoardFromFile
from BoardNode import BoardNode


def findSolution(board):
    closedBoards = {}
    openBoards = list()
    futureBoards = list()
    maxDepth = 10
    finalBoard = None

    depth = 0
    initialBoard = BoardNode(board, depth, None)
    openBoards.append(initialBoard)

    while finalBoard is None:
        while len(openBoards) > 0:
            print(str(len(openBoards)) + "/" + str(maxDepth) + " vs " + str(len(closedBoards)))
            currentBoard = openBoards.pop()

            newActions = currentBoard.exploreActions()
            for action in newActions:
                if action.key not in closedBoards:
                    if action.depth >= maxDepth:
                        futureBoards.append(action)
                    else:
                        openBoards.append(action)
                else:
                    if closedBoards[action.key].depth > action.depth:
                        ##closedBoards[action.key] = action ##TODO FIX ME SO THAT THE SHORTEST PATH IS ALWAYS FOUND
                        action.updateChildren(closedBoards)

                if action.isWon():
                    if finalBoard is None:
                        finalBoard = action
                    else:
                        if finalBoard.depth > action.depth:
                            finalBoard = action
            closedBoards[currentBoard.key] = currentBoard

        if len(openBoards) == 0 and finalBoard is None and len(futureBoards) == 0:
            print("no solution was found")
            return

        if finalBoard is None:
            print("Increasing max depth")
            maxDepth += 1
            for b in futureBoards:
                openBoards.append(b)

    finalPath = list()
    workingBoard = finalBoard
    while workingBoard.previous is not None:
        for key in closedBoards[workingBoard.previous].actionMap:
            actionTarget = closedBoards[workingBoard.previous].actionMap[key]
            if actionTarget is None:
                continue
            if actionTarget == workingBoard.key:
                finalPath.append(key)
                workingBoard = closedBoards[workingBoard.previous]
                break

    finalPath.reverse()
    finalString = ""
    for element in finalPath:
        finalString += element + "->"
    finalString += "X"
    print(finalString)

findSolution(getBoardFromFile("gamesetups/level0.txt"))
input()
findSolution(getBoardFromFile("gamesetups/level1.txt"))
input()
findSolution(getBoardFromFile("gamesetups/level2.txt"))
input()
findSolution(getBoardFromFile("gamesetups/level3.txt"))