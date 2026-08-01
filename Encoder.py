
# The Encoder module is the motion feedback system of ESP32 maze solver robot.
# Its purpose is to continuously measure the rotation of each wheel using quadrature Hall-effect encoders 
# and convert that information into meaningful data—such as distance travelled, speed, RPM, and direction
# so the robot can accurately control its movement, maintain precise positioning, support PID-based motor regulation
# and navigate the maze reliably

import math

class Encoder:
    def __init__(self, encoderA=0, encoderB=0, wheelDiaMM=0.0, ticksPerRev=1):
        self.pinA = encoderA
        self.pinB = encoderB
        self.wheelDiameter = wheelDiaMM
        self.ticksPerRevolution = ticksPerRev
        self.ticks = 0

    def begin(self):
        self.ticks = 0
        return True

    def resetTicks(self):
        self.ticks = 0

    def update(self, direction=1, tick_count=1):
        self.ticks += direction * tick_count

    def setTicks(self, ticks):
        self.ticks = ticks

    def getTicks(self):
        return self.ticks

    def getDistanceMM(self):
        circumference = math.pi * self.wheelDiameter
        return (self.ticks * circumference) / self.ticksPerRevolution

    def getDistanceCM(self):
        return self.getDistanceMM() / 10

    def getDistanceM(self):
        return self.getDistanceMM() / 1000

    def getSpeedMMps(self):
        return 0

    def getSpeedCMps(self):
        return 0

    def getRPM(self):
        return 0

    def getDirection(self):
        if self.ticks > 0:
            return 1
        elif self.ticks < 0:
            return -1
        return 0

    def simulateDistance(self, distanceMM):
        circumference = math.pi * self.wheelDiameter
        revolutions = distanceMM / circumference
        self.ticks = int(revolutions * self.ticksPerRevolution)

from Config import WHEEL_DIAMETER_MM, TICKS_PER_REV

leftEncoder = Encoder(wheelDiaMM=WHEEL_DIAMETER_MM,ticksPerRev=TICKS_PER_REV)
rightEncoder = Encoder(wheelDiaMM=WHEEL_DIAMETER_MM,ticksPerRev=TICKS_PER_REV)
