# The Maze module serves as the central environmental memory. It maintains a complete digital representation 
# of the maze by storing wall locations, visited status, and flood-fill values for every cell. As the robot explores, 
# Sensor Fusion updates this map with newly discovered walls, while the Flood Fill algorithm reads it to compute 
# the shortest path to the goal. Because all navigation decisions depend on the accuracy of this map, the Maze module
# forms the foundation upon which the robot's perception, planning, and movement systems operate.

from dataclasses import dataclass, field
from Config import MAZE_SIZE, Direction
import json
from Config import GOAL_ROW, GOAL_COL

@dataclass
class Cell:
    wall: list = field(default_factory=lambda: [False] * 4)
    visited: bool = False
    flood: int = 255

maze = [[Cell() for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

dr = (-1, 0, 1, 0)
dc = (0, 1, 0, -1)

def isInsideMaze(row, col):
    return (0 <= row < MAZE_SIZE and 0 <= col < MAZE_SIZE)

def clearMaze():
    for r in range(MAZE_SIZE):
        for c in range(MAZE_SIZE):
            maze[r][c].visited = False
            maze[r][c].flood = 255
            maze[r][c].wall = [False] * 4

def initializeMaze():
    clearMaze()
    for i in range(MAZE_SIZE):
        maze[0][i].wall[Direction.NORTH.value] = True
        maze[MAZE_SIZE - 1][i].wall[Direction.SOUTH.value] = True
        maze[i][0].wall[Direction.WEST.value] = True
        maze[i][MAZE_SIZE - 1].wall[Direction.EAST.value] = True

def initializeFlood():
    goal1 = MAZE_SIZE // 2 - 1
    goal2 = MAZE_SIZE // 2
    for r in range(MAZE_SIZE):
        for c in range(MAZE_SIZE):
            d1 = abs(r - goal1) + abs(c - goal1)
            d2 = abs(r - goal1) + abs(c - goal2)
            d3 = abs(r - goal2) + abs(c - goal1)
            d4 = abs(r - goal2) + abs(c - goal2)
            maze[r][c].flood = min(d1, d2, d3, d4)

def setVisited(row, col):
    if isInsideMaze(row, col):
        maze[row][col].visited = True

def isVisited(row, col):
    if not isInsideMaze(row, col):
        return False
    return maze[row][col].visited

def setWall(row, col, direction):
    if not isInsideMaze(row, col):
        return
    maze[row][col].wall[direction.value] = True
    nr = row + dr[direction.value]
    nc = col + dc[direction.value]
    if not isInsideMaze(nr, nc):
        return
    opposite = Direction((direction.value + 2) % 4)
    maze[nr][nc].wall[opposite.value] = True

def hasWall(row, col, direction):
    if not isInsideMaze(row, col):
        return True
    return maze[row][col].wall[direction.value]
def loadMaze(walls):
    """
    walls is a list like:
    [
        (row, col, Direction.NORTH),
        (row, col, Direction.EAST),
        ...
    ]
    """
    initializeMaze()

    for row, col, direction in walls:
        setWall(row, col, direction)

def isGoal(row, col):
    return row == GOAL_ROW and col == GOAL_COL

def removeWall(row, col, direction):
    if not isInsideMaze(row, col):
        return

    maze[row][col].wall[direction.value] = False

    nr = row + dr[direction.value]
    nc = col + dc[direction.value]

    if not isInsideMaze(nr, nc):
        return

    opposite = Direction((direction.value + 2) % 4)
    maze[nr][nc].wall[opposite.value] = False

def resetVisited():
    for r in range(MAZE_SIZE):
        for c in range(MAZE_SIZE):
            maze[r][c].visited = False

def resetFlood():
    for r in range(MAZE_SIZE):
        for c in range(MAZE_SIZE):
            maze[r][c].flood = 255

def getNeighbors(row, col):
    neighbors = []

    for direction in Direction:
        nr = row + dr[direction.value]
        nc = col + dc[direction.value]

        if isInsideMaze(nr, nc):
            neighbors.append((nr, nc, direction))

    return neighbors

def loadMazeFromJSON(filename):
    with open(filename) as f:
        config = json.load(f)

    initializeMaze()

    for wall in config["walls"]:
        direction = Direction[wall["direction"]]
        setWall(
            wall["row"],
            wall["col"],
            direction
        )

def printMaze():
    for r in range(MAZE_SIZE):
        # Top walls
        for c in range(MAZE_SIZE):
            print("+", end="")
            if maze[r][c].wall[Direction.NORTH.value]:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        # Side walls
        for c in range(MAZE_SIZE):
            if maze[r][c].wall[Direction.WEST.value]:
                print("|", end="")
            else:
                print(" ", end="")

            if maze[r][c].visited:
                print(" . ", end="")
            else:
                print("   ", end="")

        if maze[r][MAZE_SIZE-1].wall[Direction.EAST.value]:
            print("|")
        else:
            print()

    for c in range(MAZE_SIZE):
        print("+---", end="")
    print("+")

def printFlood():
    print()
    for r in range(MAZE_SIZE):
        for c in range(MAZE_SIZE):
            print(f"{maze[r][c].flood:3}", end=" ")
        print()
    print()

def printWalls():
    print()
    for r in range(MAZE_SIZE):
        for c in range(MAZE_SIZE):
            w = maze[r][c].wall
            print(f"[{int(w[0])},{int(w[1])},{int(w[2])},{int(w[3])}]", end=" ")
        print()
    print()