import pygame
import math
import copy
import random
import itertools
import numpy as np
from multiprocessing.pool import ThreadPool


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (200,200,200)
# Screen dimensions
SCREEN_WIDTH = 790
SCREEN_HEIGHT = 790

class vector:
    def __init__(self,x,y,z):
      self.x, self.y, self.z = x,y,z

    def __abs__(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def __add__(self, other):
        return vector(self.x+other.x,self.y+other.y, self.z+other.z)

    def __radd__(self, other):
        return vector(self.x+other,self.y+other, self.z+other)

    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return self.x*other.x+self.y+other.y+self.z*other.z

    def intmul(self, x):
        return vector(self.x*x, self.y*x, self.z*x)

    def __neg__(self):
        return vector(-self.x, -self.y, -self.z)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def to_2d_tuple(self):
        return (self.x,self.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False

    def __ne__(self,other):
        return not self.__eq__(other)



class Grid:

    def __init__(self, sizex, sizey):
        self.sizex =sizex
        self.sizey = sizey
        self.matrix=np.zeros((sizex, sizey))
        self.origin = (20,20)
        self.padding = 2
        self.ssize = 20

    def draw(self, screen, snake, items):
        self.drawgrid(screen)
        for i in snake.poslist:
            self.drawsquare(screen, BLACK,
                self.indexToPos(i)
                ,self.ssize)
        for item in items:
            self.drawcircle(screen, BLACK, self.indexToPos(item), self.ssize)

    def drawgrid(self, screen):
        for x in range(self.sizex):
            for y in range(self.sizey):
                self.drawsquare(screen, GREY,
                                self.indexToPos(vector(x,y,0))
                                , self.ssize)

    def indexToPos(self,vec):
        return vector(self.origin[0] + vec.x * (self.ssize + self.padding),
               self.origin[1] + vec.y * (self.ssize + self.padding),
               0)

    @staticmethod
    def drawsquare(screen, color, pos, width):
        rect = pygame.Rect(pos.x-width/2, pos.y-width/2, width, width)
        pygame.draw.rect(screen, color,  rect, 0)

    @staticmethod
    def drawcircle(screen, color, pos, width):
        pygame.draw.circle(screen, color, (pos.x, pos.y), int(width/2), 0)

    def outside(self, pos):
        if pos.x < 0 or pos.x > self.sizex-1 or pos.y < 0 or pos.y > self.sizey-1:
            return True
        else:
            return False

    def freeSquares(self,snake):
        poslist = []
        for x in range(self.sizex):
            for y in range(self.sizey):
                if vector(x,y,0) not in snake.poslist:
                    poslist.append(vector(x,y,0))
        return poslist

class Snake:

    def __init__(self, grid):
        self.length=3
        start=vector(int(grid.sizex/2),int(grid.sizey/2),0)
        self.poslist=[start]
        self.head = start
        self.dir = vector(1,0,0)

    def move(self, grid, items):
        self.poslist.append(self.head+self.dir)
        self.head = self.poslist[-1]

        if self.head in items:
            self.length += 3
            del items[items.index(self.head)]

            items.append(random.choice(grid.freeSquares(self)))
        elif len(self.poslist) == self.length+1:
            del self.poslist[0]








def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("SSSSSnake")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    items=[vector(5,5,0)]
    grid = Grid(35,35)
    snake = Snake(grid)
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == 276:
                    newdir=vector(-1,0,0)
                if event.key == 273:
                    newdir = vector(0, -1, 0)
                if event.key == 275:
                    newdir = vector(1, 0, 0)
                if event.key == 274:
                    newdir = vector(0, 1, 0)

                if snake.head+newdir != snake.poslist[-2]:
                    snake.dir=newdir

            if event.type == pygame.QUIT:
                done = True

        if grid.outside(snake.head+snake.dir) or snake.head+snake.dir in snake.poslist:
            break

        screen.fill(WHITE)


        snake.move(grid, items)
        grid.draw(screen, snake, items)


        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        # Limit to 60 frames per second

        clock.tick(7+(snake.length-3)/15)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()