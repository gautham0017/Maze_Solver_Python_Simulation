# This file acts as the central configuration file for the entire maze-solving robot. It groups together:
# Maze parameters: maze size and cell dimensions.
# Robot geometry: wheel diameter, wheel base, and derived wheel circumference.
# Encoder configuration: pulses per revolution, gear ratio, and total ticks per wheel revolution.
# Hardware pin assignments: motors, encoders, servo, and I²C.
# Sensor parameters: wall detection threshold and ToF sampling count.
# Motion settings: predefined PWM speed levels.
# Control parameters: initial PID gains.
# Servo timing: delay before taking measurements.
# Enumerations: readable names for robot directions and operating states

from math import pi
from enum import Enum

MAZE_SIZE = 8
CELL_SIZE_MM = 300.0

WHEEL_DIAMETER_MM = 30.0
WHEEL_BASE_MM = 90.0
WHEEL_CIRCUMFERENCE = pi * WHEEL_DIAMETER_MM

ENCODER_PPR = 3
GEAR_RATIO = 100
TICKS_PER_REV = ENCODER_PPR * GEAR_RATIO

SERVO_LEFT = 150
SERVO_CENTER = 90
SERVO_RIGHT = 30

WALL_THRESHOLD = 150      

SPEED_STOP = 0
SPEED_SLOW = 80
SPEED_NORMAL = 150
SPEED_FAST = 220

KP = 2.0
KI = 0.02
KD = 0.40

SERVO_SETTLE_TIME = 250     

TOF_SAMPLES = 5

MOVE_DELAY = 300

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class RobotState(Enum):
    IDLE = 0
    SCAN = 1
    FLOOD = 2
    DECIDE = 3
    MOVE = 4
    TURN_LEFT = 5
    TURN_RIGHT = 6
    TURN_BACK = 7
    SPEED_RUN = 8

# -----------------------------
# Simulator Settings
# -----------------------------

CELL_SIZE_PIXELS = 60

WINDOW_WIDTH = MAZE_SIZE * CELL_SIZE_PIXELS
WINDOW_HEIGHT = MAZE_SIZE * CELL_SIZE_PIXELS

FPS = 30
ROBOT_RADIUS = 18

GOAL_ROW = 7
GOAL_COL = 7
