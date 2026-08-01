import pygame

from Config import (MAZE_SIZE,CELL_SIZE_PIXELS,WINDOW_WIDTH,WINDOW_HEIGHT,Direction)
from Maze import maze
from Simulation import simulation
from Config import INFO_PANEL_HEIGHT,WINDOW_WIDTH

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (220, 220, 220)
        self.GREEN = (170, 255, 170)
        self.RED = (255, 60, 60)
        self.BLUE = (60, 60, 255)
        self.font = pygame.font.SysFont("Arial", 16)

    def draw(self, robot):
        self.screen.fill(self.WHITE)
        pygame.draw.rect(self.screen,(230,230,230),(0,0,WINDOW_WIDTH,INFO_PANEL_HEIGHT))
        self.drawGoal()
        self.drawVisitedCells()
        self.drawGrid()
        self.drawWalls()
        self.drawFloodValues()
        self.drawRobot(robot)
        self.drawInfo(robot)
        self.drawStatus()
        
    def drawStatus(self):
        if simulation.running:
            text = "RUNNING"
        else:
            text = "PAUSED"
        surface = self.font.render(text,True,(255,0,0))
        self.screen.blit(surface,(10,10))

    def drawVisitedCells(self):
        for r in range(MAZE_SIZE):
            for c in range(MAZE_SIZE):
                if maze[r][c].visited:
                    rect = pygame.Rect(c * CELL_SIZE_PIXELS,INFO_PANEL_HEIGHT + r * CELL_SIZE_PIXELS,CELL_SIZE_PIXELS,CELL_SIZE_PIXELS)
                    pygame.draw.rect(self.screen,self.GRAY,rect)

    def drawGoal(self):
        from Config import GOAL_ROW, GOAL_COL
        goals = [(GOAL_ROW, GOAL_COL)]
        for r, c in goals:
            rect = pygame.Rect(c * CELL_SIZE_PIXELS,INFO_PANEL_HEIGHT + r * CELL_SIZE_PIXELS,CELL_SIZE_PIXELS,CELL_SIZE_PIXELS)
            pygame.draw.rect(self.screen,self.GREEN,rect)

    def drawWalls(self):
        for r in range(MAZE_SIZE):
            for c in range(MAZE_SIZE):
                x = c * CELL_SIZE_PIXELS
                y = INFO_PANEL_HEIGHT + r * CELL_SIZE_PIXELS
                cell = maze[r][c]
                if cell.wall[Direction.NORTH.value]:
                    pygame.draw.line(self.screen,self.BLACK,(x, y),(x + CELL_SIZE_PIXELS, y),3)
                if cell.wall[Direction.EAST.value]:
                    pygame.draw.line(self.screen,self.BLACK,(x + CELL_SIZE_PIXELS, y),(x + CELL_SIZE_PIXELS, y + CELL_SIZE_PIXELS),3)
                if cell.wall[Direction.SOUTH.value]:
                    pygame.draw.line(self.screen,self.BLACK,(x, y + CELL_SIZE_PIXELS),(x + CELL_SIZE_PIXELS, y + CELL_SIZE_PIXELS),3)
                if cell.wall[Direction.WEST.value]:
                    pygame.draw.line(self.screen,self.BLACK,(x, y),(x, y + CELL_SIZE_PIXELS),3)

    def drawInfo(self, robot):
        info = [
            f"Position : ({robot.row},{robot.col})",
            f"Heading : {robot.heading.name}",
            f"Flood : {maze[robot.row][robot.col].flood}"
        ]
        y = 35
        for line in info:
            txt = self.font.render(line,True,self.BLACK)
            self.screen.blit(txt,(10,y))
            y += 20

    def drawGrid(self):
        for i in range(MAZE_SIZE + 1):
            pygame.draw.line(self.screen,(210,210,210),(0, i * CELL_SIZE_PIXELS),(WINDOW_WIDTH, i * CELL_SIZE_PIXELS),1)
            pygame.draw.line(self.screen,(210,210,210),(i * CELL_SIZE_PIXELS, 0),(i * CELL_SIZE_PIXELS, WINDOW_HEIGHT),1)

    def drawFloodValues(self):
        for r in range(MAZE_SIZE):
            for c in range(MAZE_SIZE):
                if not maze[r][c].visited:
                    continue
                value = maze[r][c].flood
                text = self.font.render(str(value),True,self.BLUE)
                rect = text.get_rect()
                rect.center = (c * CELL_SIZE_PIXELS + CELL_SIZE_PIXELS // 2,INFO_PANEL_HEIGHT + r * CELL_SIZE_PIXELS + CELL_SIZE_PIXELS // 2)
                self.screen.blit(text, rect)

    def drawRobot(self, robot):
        cx = robot.col * CELL_SIZE_PIXELS + CELL_SIZE_PIXELS // 2
        cy = INFO_PANEL_HEIGHT + robot.row * CELL_SIZE_PIXELS + CELL_SIZE_PIXELS // 2
        radius = CELL_SIZE_PIXELS // 3
        pygame.draw.circle(self.screen,self.RED,(cx, cy),radius)
        pygame.draw.circle(self.screen,self.BLACK,(cx, cy),radius,2)
        if robot.heading == Direction.NORTH:
            end = (cx, cy - radius)
        elif robot.heading == Direction.EAST:
            end = (cx + radius, cy)
        elif robot.heading == Direction.SOUTH:
            end = (cx, cy + radius)
        else:
            end = (cx - radius, cy)
        pygame.draw.line(self.screen,self.BLACK,(cx, cy),end,4)
