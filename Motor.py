# The Motor module is the low-level motion control layer of the ESP32 maze solver robot.
# Its purpose is to translate high-level movement commands into precise electrical control signals
# for the DRV8833 motor driver, enabling accurate control of motor direction, speed, stopping, 
# and braking so the robot can execute the navigation decisions made by the Flood Fill algorithm and other control systems.

class Motor:
    def __init__(self, pin1=0, pin2=0):
        self.in1 = pin1
        self.in2 = pin2
        self.currentSpeed = 0

    def begin(self):
        self.currentSpeed = 0
        return True

    def forward(self, pwm):
        self.currentSpeed = max(0, min(int(pwm), 255))

    def backward(self, pwm):
        self.currentSpeed = -max(0, min(int(pwm), 255))

    def stop(self):
        self.currentSpeed = 0

    def brake(self):
        self.stop()

    def setSpeed(self, pwm):
        self.currentSpeed = max(-255, min(int(pwm), 255))

    def getSpeed(self):
        return self.currentSpeed

    def isRunning(self):
        return self.currentSpeed != 0