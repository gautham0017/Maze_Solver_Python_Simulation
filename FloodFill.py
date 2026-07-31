# the Flood Fill module is the path-planning algorithm that converts the robot's discovered maze map 
# into an optimal route toward the goal. Using Breadth-First Search (BFS), it propagates distance values
# from the goal through every reachable cell, creating a gradient that always points toward the shortest known path. 
# As the robot discovers new walls, these flood values are recalculated, allowing the robot to dynamically adapt its route, 
# avoid dead ends, and efficiently navigate to the maze center.

from collections import deque

from Config import MAZE_SIZE, Direction
from Maze import (maze,initializeMaze,initializeFlood,printFlood)
from Maze import resetFlood
from Config import GOAL_ROW, GOAL_COL

dr = (-1, 0, 1, 0)
dc = (0, 1, 0, -1)

class FloodFill:
    def __init__(self):
        self.queue = deque()

    def initialize(self):
        initializeFlood()

    def clearQueue(self):
        self.queue.clear()

    def isQueueEmpty(self):
        return len(self.queue) == 0

    def enqueue(self, row, col):
        self.queue.append((row, col))

    def dequeue(self):
        return self.queue.popleft()

    def isValidCell(self, row, col):
        return (0 <= row < MAZE_SIZE and 0 <= col < MAZE_SIZE)

    def canMove(self, row, col, direction):
        if not self.isValidCell(row, col):
            return False
        return not maze[row][col].wall[direction.value]

    def updateFloodValues(self):
        resetFlood()
        self.clearQueue()
        maze[GOAL_ROW][GOAL_COL].flood = 0
        self.enqueue(GOAL_ROW, GOAL_COL)

        while not self.isQueueEmpty():
            row, col = self.dequeue()
            currentFlood = maze[row][col].flood
            for direction in Direction:
                if not self.canMove(row, col, direction):
                    continue
                nr = row + dr[direction.value]
                nc = col + dc[direction.value]
                if not self.isValidCell(nr, nc):
                    continue
                if maze[nr][nc].flood > currentFlood + 1:
                    maze[nr][nc].flood = currentFlood + 1
                    self.enqueue(nr, nc)

    def getBestDirection(self, row, col):
        bestFlood = maze[row][col].flood
        bestDirection = None

        for direction in Direction:
            if not self.canMove(row, col, direction):
                continue

            nr = row + dr[direction.value]
            nc = col + dc[direction.value]

            if not self.isValidCell(nr, nc):
                continue

            if maze[nr][nc].flood < bestFlood:
                bestFlood = maze[nr][nc].flood
                bestDirection = direction
        return bestDirection

    def reachedGoal(self, row, col):
        center1 = MAZE_SIZE // 2 - 1
        center2 = MAZE_SIZE // 2
        return (row, col) in [
    (center1, center1),
    (center1, center2),
    (center2, center1),
    (center2, center2)
]
    def isSolved(self, row, col):
        return self.reachedGoal(row, col)

    def printCurrentCell(self, row, col):
        print(
        f"Cell ({row},{col}) Flood =",
        maze[row][col].flood
    )

    def getPath(self, row, col):
        path = []
        while not self.reachedGoal(row, col):
            direction = self.getBestDirection(row, col)
            path.append(direction)
            row += dr[direction.value]
            col += dc[direction.value]
        return path

    def printFloodValues(self):
        printFlood()

floodFill = FloodFill()