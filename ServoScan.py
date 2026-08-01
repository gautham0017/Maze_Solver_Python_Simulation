# The ServoScanner module is the active environmental scanning system of maze solver robot. 
# Its purpose is to precisely position the ToF sensor toward the left, front, and right directions, 
# collect stable distance measurements from each viewpoint, and provide a complete local view of the maze
# so that the robot can accurately detect walls, update its internal map, and make intelligent navigation decisions.

from dataclasses import dataclass
from Config import Direction
from Maze import maze

@dataclass
class ScanResult:
    left: int = 0
    front: int = 0
    right: int = 0

class ServoScanner:
    WALL_DISTANCE = 50
    OPEN_DISTANCE = 1000

    def __init__(self):
        self.robot = None

    def begin(self, robot=None):
        self.robot = robot
        return True

    def wallToDistance(self, wall):
        if wall:
            return self.WALL_DISTANCE
        return self.OPEN_DISTANCE

    def scan_(self):
        if self.robot is None:
            return ScanResult(self.OPEN_DISTANCE,self.OPEN_DISTANCE,self.OPEN_DISTANCE)

    def scan(self):
        result = ScanResult()
        row = self.robot.row
        col = self.robot.col
        heading = self.robot.heading
        cell = maze[row][col]
        if heading == Direction.NORTH:
            result.left = self.wallToDistance(cell.wall[Direction.WEST.value])
            result.front = self.wallToDistance(cell.wall[Direction.NORTH.value])
            result.right = self.wallToDistance(cell.wall[Direction.EAST.value])
        elif heading == Direction.EAST:
            result.left = self.wallToDistance(cell.wall[Direction.NORTH.value])
            result.front = self.wallToDistance(cell.wall[Direction.EAST.value])
            result.right = self.wallToDistance(cell.wall[Direction.SOUTH.value])
        elif heading == Direction.SOUTH:
            result.left = self.wallToDistance(cell.wall[Direction.EAST.value])
            result.front = self.wallToDistance(cell.wall[Direction.SOUTH.value])
            result.right = self.wallToDistance(cell.wall[Direction.WEST.value])
        elif heading == Direction.WEST:
            result.left = self.wallToDistance(cell.wall[Direction.SOUTH.value])
            result.front = self.wallToDistance(cell.wall[Direction.WEST.value])
            result.right = self.wallToDistance(cell.wall[Direction.NORTH.value])
        return result

scanner = ServoScanner()
