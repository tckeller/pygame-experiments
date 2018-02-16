import pygame
import math
import copy
import random
from multiprocessing.pool import ThreadPool


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (150,150,150)
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

g=0.01

def draw_arrow(start, end, width, color, screen):
    pygame.draw.line(screen, color, start.to_2d_tuple(), end.to_2d_tuple(), width)

def gravity(x,y):
    try:
        return -(x.pos-y.pos).intmul(g*(x.m*y.m)/abs(x.pos-y.pos)**2)
    except:
        return 0

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


import threading
def physics(universe, dt):
    threads = []
    new_universe= []
    F = vector(0,0,0)
    com_g = COM_global([p for p in universe])
    M_g = sum([p.m for p in universe])
    for i, p in enumerate(universe):
        try:
            F = gravity(p,particle(COM_indiv(com_g, M_g, p), vector(0,0,0), M_g-p.m))
        except:
            F=vector(0,0,0)
        p.move(F,dt)

    return universe

def COM_global(universe):
    return sum([p.pos.intmul(p.m) for p in universe]).intmul(1.0/sum([p.m for p in universe]))

def COM_indiv(COM_glob, M_glob, prtcl):
    return (COM_glob - prtcl.pos.intmul(prtcl.m).intmul(1/(M_glob))).intmul(M_glob/(M_glob-prtcl.m))

def move_from_universe(prtcl , universe, dt):
    prtcl = copy.deepcopy(prtcl)

    F = vector(0,0,0)
    com = COM_global([p for p in universe if p!=prtcl])
    M = sum([p.m for p in universe if p!=prtcl])
    F += gravity(prtcl,particle(com, vector(0,0,0), M))
    prtcl.move(F,dt)
    return prtcl

class particle:

    def __init__(self, pos, vel, rad):
        self.density = 10e-4
        self.pos = pos
        self.vel = vel
        self.rad = rad
        self.m = self.density * math.pi * self.rad ** 3

    def update_mass(self):
        self.m = self.density * math.pi * self.rad ** 3

    def move(self, F, dt):
        self.pos = self.pos + self.vel.intmul(dt) + F.intmul(0.5*dt**2/self.m)
        self.vel = self.vel + F.intmul(dt/self.m)
        self.reflect()

    def draw(self, screen):
        pygame.draw.circle(screen, GREY, (int(self.pos.x), int(self.pos.y)), int(self.rad), 0)

    def reflect(self):
        if self.pos.x < 0 or self.pos.x > SCREEN_WIDTH:
            self.vel.x = -self.vel.x
        if  self.pos.y < 0 or self.pos.y > SCREEN_HEIGHT:
            self.vel.y = -self.vel.y







def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Universe Sim")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Set up particles

    grid_size = 10
    padding = 10
    universe = []
    for i in range(grid_size):
        for j in range(grid_size):
            universe.append(particle(vector(random.randint(1, SCREEN_WIDTH),
                                            random.randint(1, SCREEN_HEIGHT), 0),
                                     vector(0,0,0),
                                     random.randint(1,20)
                                     )
                            )


    done = False#
    new_prtcl = None
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                new_prtcl = particle(vector(event.pos[0], event.pos[1], 0), vector(0,0,0), 2)

            if event.type == pygame.MOUSEBUTTONUP:
                new_prtcl.update_mass()
                print new_prtcl.m
                universe.append(copy.deepcopy(new_prtcl))
                new_prtcl = None

        screen.fill(WHITE)

        if new_prtcl is not None:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = vector(mouse_pos[0], mouse_pos[1], 0)
            draw_arrow(new_prtcl.pos, new_prtcl.pos.intmul(2)-mouse_pos, 2, BLACK, screen)
            new_prtcl.vel = new_prtcl.pos-mouse_pos
            new_prtcl.rad += 0.1
            new_prtcl.draw(screen)

        TicksPerUpdate = 50
        if len(universe) > 0:
            for i in range(TicksPerUpdate):
                universe = physics(universe,1/float(TicksPerUpdate*60))
        for p in universe:
            p.draw(screen)


        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()