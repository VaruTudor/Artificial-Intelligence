
# import the pygame module, so you can use it

import time
import pygame

from random import randint

# Creating some colors
from Domain import Map, Drone
from Service import Service

BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

START_X = 5
START_Y = 12
FINAL_X = 14
FINAL_Y = 11
TIME_BETWEEN_MOVES = 0.4


class View:
    @staticmethod
    def run():
        # we create the map
        m = Map()
        # m.randomMap()
        # m.saveMap("test2.map")
        m.loadMap("util/test1.map")

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("util/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # we position the drone somewhere in the area
        x = START_X
        # x = randint(0, 19)
        y = START_Y
        # y = randint(0, 19)

        # create drona
        drone = Drone(x, y)

        service = Service(drone, m)

        startTime = time.time()
        uniformPath = service.searchUniformCost(FINAL_X, FINAL_Y)
        # uniformPath = service.searchUniformCost(service.getDrone().x-3, service.getDrone().y+3)
        print("\n uniform path  " + uniformPath.__str__() +
              "\n uniform path-find : %s seconds\n" % (time.time() - startTime))

        startTime = time.time()
        greedyPath = service.searchGreedy(FINAL_X, FINAL_Y)
        # greedyPath = service.searchGreedy(service.getDrone().x-3, service.getDrone().y+3)
        path = service.transform(greedyPath)
        print("\n greedy path   " + greedyPath.__str__() +
              "\n greedy path-find  : %s seconds\n" % (time.time() - startTime))

        startTime = time.time()
        aStarPath = service.searchAStar(FINAL_X, FINAL_Y)
        # aStarPath = service.searchAStar(service.getDrone().x-3, service.getDrone().y+3)
        print("\n A* path       " + aStarPath.__str__() +
              "\n A* path-find      : %s seconds\n" % (time.time() - startTime))

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)

        # define a variable to control the main loop
        running = True

        path = [(6,2),(7,2)]

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            if path.__len__() > 0:
                position = path.pop(0)
                time.sleep(TIME_BETWEEN_MOVES)
                drone.moveTo(position[0], position[1])
                screen.blit(drone.mapWithDrone(m.image()), (0, 0))
                pygame.display.flip()
            else:
                screen.blit(service.displayWithPath(m.image(), path), (0, 0))
                pygame.display.flip()

        pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    View.run()
