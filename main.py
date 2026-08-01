
import pygame
import sys
import time

from Config import (Direction,RobotState,FPS,WINDOW_WIDTH,WINDOW_HEIGHT,)
from Robot import Robot
from Renderer import Renderer
from MazeLoader import loadMazeFromFile
from Simulation import simulation

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Solver Simulator")
    clock = pygame.time.Clock()
    renderer = Renderer(screen)
    robot = Robot()
    loadMazeFromFile()
    robot.begin()
    robot.setPosition(0, 0)
    robot.setHeading(Direction.NORTH)
    robot.setState(RobotState.SCAN)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation.start()
                elif event.key == pygame.K_p:
                    simulation.pause()
                elif event.key == pygame.K_r:
                    robot = Robot()
                    robot.begin()
                    robot.setPosition(0,0)
                    robot.setHeading(Direction.NORTH)
                    robot.setState(RobotState.SCAN)
                    simulation.reset()
                elif event.key == pygame.K_n:
                    simulation.nextStep()
        if simulation.running:
            robot.update()
        elif simulation.step:
            robot.update()
            simulation.step = False
        if robot.isSolved():
            print("Simulation Finished!")
            running = False
        renderer.draw(robot)
        pygame.display.flip()
        time.sleep(0.2)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
