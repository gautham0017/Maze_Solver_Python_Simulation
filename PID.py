# The PID module is the real-time motion correction system of the maze solver robot. 
# Its purpose is to use sensor feedback to continuously detect movement errors and automatically 
# adjust the motor outputs, ensuring the robot drives straight, turns accurately, maintains stable speed,
# and navigates the maze with the precision required for successful exploration and fast speed runs.

class PIDController:

    def __init__(self, kp=0.0, ki=0.0, kd=0.0):
        
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.error = 0.0
        self.previousError = 0.0

        self.integral = 0.0
        self.derivative = 0.0

        self.minOutput = -255.0
        self.maxOutput = 255.0

        self.integralMin = -1000.0
        self.integralMax = 1000.0

    def begin(self):
        self.reset()

    def compute(self, setpoint, measurement, dt):        
        if dt <= 0:
            return 0.0
        self.error = setpoint - measurement
        self.integral += self.error * dt
        self.integral = max(self.integralMin,min(self.integral, self.integralMax))
        self.derivative = (self.error - self.previousError) / dt

        output = (self.kp * self.error +self.ki * self.integral +self.kd * self.derivative)
        output = max(self.minOutput,min(output, self.maxOutput))
        self.previousError = self.error
        return output

    def reset(self):
        self.error = 0.0
        self.previousError = 0.0
        self.integral = 0.0
        self.derivative = 0.0

    def setKp(self, kp):
        self.kp = kp

    def setKi(self, ki):
        self.ki = ki

    def setKd(self, kd):
        self.kd = kd

    def setOutputLimits(self, minimum, maximum):
        self.minOutput = minimum
        self.maxOutput = maximum

    def setIntegralLimits(self, minimum, maximum):
        self.integralMin = minimum
        self.integralMax = maximum

    def getKp(self):
        return self.kp

    def getKi(self):
        return self.ki

    def getKd(self):
        return self.kd

    def getError(self):
        return self.error

    def getIntegral(self):
        return self.integral

    def getDerivative(self):
        return self.derivative