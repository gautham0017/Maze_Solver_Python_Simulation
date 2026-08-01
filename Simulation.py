class Simulation:
    def __init__(self):
        self.running = False
        self.step = False

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def toggle(self):
        self.running = not self.running

    def reset(self):
        self.running = False
        self.step = False

    def nextStep(self):
        self.step = True

simulation = Simulation()