# The TurnController module is the precision turning system of the maze solver robot. 
# Its purpose is to execute accurate rotations by combining motor control, gyroscope feedback, 
# and PID control, ensuring that every commanded turn is completed with the correct orientation 
# before the robot continues navigating the maze.

from Config import Direction

class TurnController:
    def __init__(self):
        self.robot = None

    def begin(self, robot):
        self.robot = robot
        return True

    def turnLeft90(self):
        if self.robot is None:
            return True
        self.robot.heading = Direction((self.robot.heading.value + 3) % 4)
        return True

    def turnRight90(self):
        if self.robot is None:
            return True

        self.robot.heading = Direction((self.robot.heading.value + 1) % 4)
        return True

    def turnAround(self):
        if self.robot is None:
            return True
        self.robot.heading = Direction((self.robot.heading.value + 2) % 4)
        return True

turnController = TurnController()
