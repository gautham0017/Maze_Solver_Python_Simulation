# For the ESP32-based maze-solving robot, the Navigation module serves as the central mission controller. 
# It keeps track of the robot's position, heading, and current mission phase while coordinating Sensor Fusion, 
# the Maze module, Flood Fill, and the Motion Controller. By repeatedly scanning the environment, updating the maze, 
# selecting the best direction, and commanding the required movements, it enables the robot to autonomously explore the maze, 
# reach the goal, return home, and prepare for an optimized fast run.

from dataclasses import dataclass

from Config import MAZE_SIZE, Direction
from FloodFill import FloodFill
from Motion_Controller import MotionController

class RobotHeading:
    HEADING_NORTH = Direction.NORTH
    HEADING_EAST = Direction.EAST
    HEADING_SOUTH = Direction.SOUTH
    HEADING_WEST = Direction.WEST

class NavigationState:
    NAV_EXPLORE = 0
    NAV_RETURN_HOME = 1
    NAV_FAST_RUN_READY = 2
    NAV_FAST_RUN = 3
    NAV_FINISHED = 4

@dataclass
class RobotState:
    row: int
    col: int
    heading: Direction

class Navigation:
    def __init__(self):
        self.robot = RobotState(MAZE_SIZE - 1,0, Direction.NORTH)
        self.state = NavigationState.NAV_EXPLORE
        self.motion = None
        self.sensors = None
        self.flood = None

    def begin(self,motionController,sensorFusion,floodFill):
        self.motion = motionController
        self.sensors = sensorFusion
        self.flood = floodFill
        self.robot.row = MAZE_SIZE - 1
        self.robot.col = 0
        self.robot.heading = Direction.NORTH
        self.state = NavigationState.NAV_EXPLORE

    def getRobotState(self):
        return self.robot
    
    def getNavigationState(self):
        return self.state

    def setPosition(self, row, col):
        self.robot.row = row
        self.robot.col = col

    def setHeading(self, heading):
        self.robot.heading = heading

    def goalReached(self):
        return self.flood.reachedGoal(self.robot.row,self.robot.col)

    def missionFinished(self):
        return (self.state ==NavigationState.NAV_FINISHED)

    def leftOf(self, direction):
        return Direction((direction.value - 1) % 4)

    def rightOf(self, direction):
        return Direction((direction.value + 1) % 4)

    def oppositeOf(self, direction):
        return Direction((direction.value + 2) % 4)

    def directionDifference(self,current,target):
        return (target.value -current.value +4) % 4

    def updateHeading(self, direction):
        self.robot.heading = direction

    def updatePosition(self):
        if self.robot.heading == Direction.NORTH:
            if self.robot.row > 0:
                self.robot.row -= 1
        elif self.robot.heading == Direction.EAST:
            if self.robot.col < MAZE_SIZE - 1:
                self.robot.col += 1
        elif self.robot.heading == Direction.SOUTH:
            if self.robot.row < MAZE_SIZE - 1:
                self.robot.row += 1
        elif self.robot.heading == Direction.WEST:
            if self.robot.col > 0:
                self.robot.col -= 1

    def rotateTo(self, target):
        if self.robot.heading == target:
            return
        diff = self.directionDifference(self.robot.heading,target)
        if diff == 1:
            while not self.motion.turnRight90():
                pass
        elif diff == 2:
            while not self.motion.turnAround():
                pass
        elif diff == 3:
            while not self.motion.turnLeft90():
                pass
        self.updateHeading(target)
        self.motion.stop()

    def moveOneCell(self):
        while not self.motion.driveOneCell():
            pass
        self.motion.stop()
        self.updatePosition()

    def printRobotState(self):
        print()
        print("========== ROBOT ==========")
        print(f"Row      : {self.robot.row}")
        print(f"Column   : {self.robot.col}")
        print(f"Heading  : {self.robot.heading.name}")
        state_names = {
            NavigationState.NAV_EXPLORE:
                "EXPLORE",
            NavigationState.NAV_RETURN_HOME:
                "RETURN HOME",
            NavigationState.NAV_FAST_RUN_READY:
                "FAST RUN READY",
            NavigationState.NAV_FAST_RUN:
                "FAST RUN",
            NavigationState.NAV_FINISHED:
                "FINISHED"
        }

        print("State    :",state_names[self.state])
        print()

    def exploreStep(self):
        self.sensors.scanWalls(self.robot.row,self.robot.col,self.robot.heading)
        self.flood.updateFloodValues()
        if self.goalReached():
            print("Center Reached")
            self.state = (NavigationState.NAV_RETURN_HOME)
            return
        direction = self.flood.getBestDirection(
            self.robot.row,
            self.robot.col
        )
        self.rotateTo(direction)
        self.moveOneCell()
 
    def returnStep(self):
        self.sensors.scanWalls(
            self.robot.row,
            self.robot.col,
            self.robot.heading
        )
        self.flood.updateFloodValues()
        if (self.robot.row == MAZE_SIZE - 1 and self.robot.col == 0):
            print("Returned Home")
            self.state = (NavigationState.NAV_FAST_RUN_READY)
            return

        direction = self.flood.getBestDirection(self.robot.row,self.robot.col)
        self.rotateTo(direction)
        self.moveOneCell()

    def fastRunStep(self):
        print("Fast Run Mode")
        self.state = (
            NavigationState.NAV_FINISHED
        )

    def update(self):
        if self.state == NavigationState.NAV_EXPLORE:
            self.exploreStep()
        elif self.state == NavigationState.NAV_RETURN_HOME:
            self.returnStep()
        elif self.state == NavigationState.NAV_FAST_RUN_READY:
            print("Preparing Fast Run")
            self.state = (
                NavigationState.NAV_FAST_RUN
            )
        elif self.state == NavigationState.NAV_FAST_RUN:
            self.fastRunStep()
        elif self.state == NavigationState.NAV_FINISHED:
            self.motion.stop()

navigation = Navigation()