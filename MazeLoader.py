import json
from Config import Direction
from Maze import loadMaze

def loadMazeFromFile(filename="maze_config.json"):
    with open(filename, "r") as file:
        data = json.load(file)
    walls = []
    for wall in data["walls"]:
        direction = Direction[wall["direction"]]
        walls.append((wall["row"],wall["col"],direction))
    loadMaze(walls)
    return data
