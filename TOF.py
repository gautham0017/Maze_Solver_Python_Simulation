# The TOF module is the perception system of the maze solver robot. Its purpose is to accurately 
# measure the distance to surrounding walls using the VL53L0X Time-of-Flight sensor, providing reliable 
# environmental information that allows the robot to detect obstacles, construct an internal map of the maze, 
# and make intelligent navigation decisions.

from collections import deque
from statistics import median
from collections import deque
from statistics import median
from Config import WALL_THRESHOLD

WALL_DISTANCE = 50      # Wall detected
OPEN_DISTANCE = 1000    # No wall

class TOFSensor:
    FILTER_SIZE = 5
    def __init__(self):
        self.lastDistance = OPEN_DISTANCE
        self.initialized = False
        self.timeout = False
        self.samples = deque([OPEN_DISTANCE] * self.FILTER_SIZE,maxlen=self.FILTER_SIZE)

    def begin(self):
        self.initialized = True
        return True

    def setDistance(self, distance):
        self.lastDistance = distance
        self.samples.append(distance)
        self.timeout = False

    def wallDetected(self):
        return self.getFilteredDistance() < WALL_THRESHOLD

    def getDistance(self):
        return self.lastDistance

    def setDistance(self, distance):
        if not self.initialized:
            return
        self.lastDistance = distance
        self.samples.append(distance)
        self.timeout = False

    def medianFilter(self):
        return int(median(self.samples))

    def getFilteredDistance(self):
        return self.medianFilter()

    def simulateTimeout(self):
        self.timeout = True

    def isTimeout(self):
        return self.timeout

    def reset(self):
        self.lastDistance = OPEN_DISTANCE
        self.samples = deque([OPEN_DISTANCE] * self.FILTER_SIZE,maxlen=self.FILTER_SIZE)
        self.timeout = False

tof = TOFSensor()
