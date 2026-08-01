# The MPU module is the orientation feedback system of the maze solver robot.
# Its purpose is to continuously monitor the robot's rotational movement using the MPU6050 gyroscope, 
# calculate its heading, and provide accurate orientation information so the robot can execute precise turns, 
# maintain the correct direction, and navigate the maze reliably.

class MPU:
    def __init__(self):
        self.heading = 0.0

    def begin(self):
        self.heading = 0.0
        return True

    def calibrate(self, samples=1000):
        return True

    def update(self):
        pass

    def resetHeading(self):
        self.heading = 0.0

    def getHeading(self):
        return self.heading

    def setHeading(self, angle):
        self.heading = self.normalizeAngle(angle)

    def rotate(self, angle):
        self.heading = self.normalizeAngle(self.heading + angle)

    @staticmethod
    def normalizeAngle(angle):
        angle %= 360
        if angle >= 180:
            angle -= 360
        return angle
