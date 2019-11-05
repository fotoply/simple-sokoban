availableOptions = ["u", "d", "l", "r"]

class BoardNode:
    def __init__(self, state, depth, previous):
        self.state = state
        self.key = self.getHash(self.state)
        self.depth = depth
        self.previous = previous
        self.actionMap = {}
        self.won = False

    def getHash(self, state):
        playerHash = ""
        moveableHash = ""
        for y in range(len(state)):
            for x in range(len(state[y])):
                cell = state[y][x]
                if cell == "p":
                    playerHash = str(y).zfill(2) + str(x).zfill(2)
                elif cell == "m":
                    moveableHash += str(y).zfill(2) + str(x).zfill(2)
        return playerHash + moveableHash

    def isWon(self):
        return self.won

    def exploreActions(self):
        global availableOptions
        from board import Board
        furtherActions = list()
        for option in availableOptions:
            board = Board()
            board.initBoard(self.state)
            board.move(option)
            boardState = board.getBoard()
            if self.getHash(boardState) != self.key:
                newAction = BoardNode(boardState, self.depth + 1, self.key)
                newAction.won = board.isGameWon()
                self.actionMap[option] = newAction.key
                furtherActions.append(newAction)
            else:
                self.actionMap[option] = None

        return furtherActions
