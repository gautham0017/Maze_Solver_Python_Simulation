# The Robot class is the central brain and coordinator of  ESP32 maze solver robot. 
# It maintains the robot's current position,orientation, sensor information, and operating state, 
# while orchestrating the interaction between all hardware modules (motors, encoders, sensors) and 
# software modules (PID, maze mapping, flood fill, and navigation) so the robot can continuously 
# sense its environment, make intelligent decisions, and navigate through the maze autonomously.

from Config import Direction, RobotState, WALL_THRESHOLD
from Maze import maze, setWall, setVisited
from FloodFill import floodFill
from Motion_Controller import motion
from ServoScan import scanner
from MPU import MPU

class Robot:

    def __init__(self):
        self.row = 0
        self.col = 0
        self.heading = Direction.NORTH
        self.state = RobotState.IDLE
        self.leftDistance = 0
        self.frontDistance = 0
        self.rightDistance = 0
        self.imu = MPU()
        self.initialized = False
        self.solved = False

    def begin(self):
        self.imu.begin()
        motion.begin(self)
        scanner.begin(self)
        floodFill.initialize()
        self.initialized = True
        print("Robot Initialized")

    def update(self):
        if not self.initialized:
            return
        if self.state == RobotState.IDLE:
            return
        elif self.state == RobotState.SCAN:
            self.scanWalls()
        elif self.state == RobotState.FLOOD:
            self.computeFlood()
        elif self.state == RobotState.DECIDE:
            self.decideNextMove()
        elif self.state == RobotState.MOVE:
            self.moveForward()
        elif self.state == RobotState.TURN_LEFT:
            self.turnLeft()
        elif self.state == RobotState.TURN_RIGHT:
            self.turnRight()
        elif self.state == RobotState.TURN_BACK:
            self.turnBack()
        elif self.state == RobotState.SPEED_RUN:
            pass

    def setPosition(self, row, col):
        self.row = row
        self.col = col

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def setHeading(self, heading):
        self.heading = heading

    def getHeading(self):
        return self.heading

    def setDistances(self, left, front, right):
        self.leftDistance = left
        self.frontDistance = front
        self.rightDistance = right

    def getLeftDistance(self):
        return self.leftDistance

    def getFrontDistance(self):
        return self.frontDistance

    def getRightDistance(self):
        return self.rightDistance

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def moveForward(self):
        motion.driveOneCell()
        if self.frontDistance < WALL_THRESHOLD:
            print("Blocked!")
            self.state = RobotState.SCAN
            return
        if self.heading == Direction.NORTH:
            self.row -= 1
        elif self.heading == Direction.EAST:
            self.col += 1
        elif self.heading == Direction.SOUTH:
            self.row += 1
        elif self.heading == Direction.WEST:
            self.col -= 1
        self.row = max(0, min(self.row, len(maze) - 1))
        self.col = max(0, min(self.col, len(maze[0]) - 1))
        self.printStatus()
        self.state = RobotState.SCAN

    def turnLeft(self):
        motion.turnLeft90()
        self.imu.setHeading(self.heading.value * 90)
        self.printStatus()
        self.state = RobotState.MOVE

    def turnRight(self):
        motion.turnRight90()
        self.imu.setHeading(self.heading.value * 90)
        self.printStatus()
        self.state = RobotState.MOVE

    def turnBack(self):
        motion.turnAround()
        self.imu.setHeading(self.heading.value * 90)
        self.printStatus()
        self.state = RobotState.MOVE

    def scanWalls(self):
        result = scanner.scan()
        self.leftDistance = result.left
        self.frontDistance = result.front
        self.rightDistance = result.right
        self.updateMaze()
        self.printStatus()
        self.state = RobotState.FLOOD

    def updateMaze(self):
        if not (0 <= self.row < len(maze)and 0 <= self.col < len(maze[0])):
            return

        # Mark current cell as visited
        setVisited(self.row, self.col)

        leftWall = self.leftDistance < WALL_THRESHOLD
        frontWall = self.frontDistance < WALL_THRESHOLD
        rightWall = self.rightDistance < WALL_THRESHOLD

        if self.heading == Direction.NORTH:
            if leftWall:
                setWall(self.row, self.col, Direction.WEST)
            if frontWall:
                setWall(self.row, self.col, Direction.NORTH)
            if rightWall:
                setWall(self.row, self.col, Direction.EAST)
        elif self.heading == Direction.EAST:
            if leftWall:
                setWall(self.row, self.col, Direction.NORTH)
            if frontWall:
                setWall(self.row, self.col, Direction.EAST)
            if rightWall:
                setWall(self.row, self.col, Direction.SOUTH)

        elif self.heading == Direction.SOUTH:
            if leftWall:
                setWall(self.row, self.col, Direction.EAST)
            if frontWall:
                setWall(self.row, self.col, Direction.SOUTH)
            if rightWall:
                setWall(self.row, self.col, Direction.WEST)
        elif self.heading == Direction.WEST:
            if leftWall:
                setWall(self.row, self.col, Direction.SOUTH)
            if frontWall:
                setWall(self.row, self.col, Direction.WEST)
            if rightWall:
                setWall(self.row, self.col, Direction.NORTH)

    def computeFlood(self):
        floodFill.updateFloodValues()
        self.state = RobotState.DECIDE

        if floodFill.reachedGoal(self.row, self.col):
            print("Maze Solved!")
            self.solved = True
            self.state = RobotState.IDLE

    def decideNextMove(self):
        best = floodFill.getBestDirection(self.row,self.col)
        if best is None:
            self.state = RobotState.IDLE
            return
        if best == self.heading:
            self.state = RobotState.MOVE
        elif best == Direction((self.heading.value + 3) % 4):
            self.state = RobotState.TURN_LEFT
        elif best == Direction((self.heading.value + 1) % 4):
            self.state = RobotState.TURN_RIGHT
        else:
            self.state = RobotState.TURN_BACK

    def isSolved(self):
        return self.solved

    # Debug
    def printStatus(self):
        print("=" * 35)
        print(f"Position : ({self.row}, {self.col})")
        print(f"Heading  : {self.heading.name}")
        print(f"State    : {self.state.name}")
        print(f"Left     : {self.leftDistance}")
        print(f"Front    : {self.frontDistance}")
        print(f"Right    : {self.rightDistance}")
        print("=" * 35)