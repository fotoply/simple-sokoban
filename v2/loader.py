import os
import sys

def getBoardFromFile(path):
    board = []
    location = os.path.join(sys.path[0], path)
    with open(location, 'r') as file:
        for line in file:
            line.replace("\n", "")
            chars = list(line)
            board.append(chars)
    return board