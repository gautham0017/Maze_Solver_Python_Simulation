# The MotionController is the robot's movement engine: it takes movement commands from the Navigation module
# and uses the motors, encoders, MPU6050, PID controller, and TurnController to execute precise, reliable movements 
# from one maze cell to the next while maintaining accuracy.

from Config import CELL_SIZE_MM, TICKS_PER_REV
from Encoder import leftEncoder, rightEncoder
from MPU import MPU
from TurnController import turnController

class MotionController:
    def __init__(self):
        self.robot = None
        self.leftEncoder = leftEncoder
        self.rightEncoder = rightEncoder
        self.imu = MPU()
        self.cellDistance = CELL_SIZE_MM
        self.initialized = False
        self.travelledDistance = 0

    def begin(self, robot):
        self.robot = robot
        self.imu = robot.imu
        self.leftEncoder.begin()
        self.rightEncoder.begin()
        self.imu.begin()
        turnController.begin(robot)
        self.initialized = True
        return True

    def isInitialized(self):
        return self.initialized
    
    def resetEncoders(self):
        self.leftEncoder.resetTicks()
        self.rightEncoder.resetTicks()

    def driveDistance(self, distanceMM):
        self.resetEncoders()
        self.leftEncoder.update(1, TICKS_PER_REV)
        self.rightEncoder.update(1, TICKS_PER_REV)
        self.travelledDistance += distanceMM
        self.imu.update()
        return True

    def getDistanceTravelled(self):
        return self.travelledDistance

    def driveOneCell(self):
        return self.driveDistance(self.cellDistance)

    def turnLeft90(self):
        if not self.initialized:
            return True
        return turnController.turnLeft90()

    def turnRight90(self):
        if not self.initialized:
            return True
        return turnController.turnRight90()

    def turnAround(self):
        if not self.initialized:
            return True
        return turnController.turnAround()

    def stop(self):
        self.resetEncoders()

motion = MotionController()
