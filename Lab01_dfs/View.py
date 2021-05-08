import time

import pygame
from random import randint

from Domain import Environment, Drone, DMap
from Service import Service

# Creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TIME_BETWEEN_MOVES = 0.3


class View:
    @staticmethod
    def run():
        # we create the environment
        e = Environment()
        e.loadEnvironment("util/test2.map")
        # print(str(e))

        # we create the map
        m = DMap()

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("util/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # we position the drone somewhere in the area
        x = randint(0, 19)
        y = randint(0, 19)

        # cream drona
        d = Drone(x, y)

        service = Service(d, e)

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)
        screen.blit(service.get_environment().imageR(), (0, 0))

        # define a variable to control the main loop
        keep_running = True

        # main loop
        while keep_running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    keep_running = False
            try:
                time.sleep(TIME_BETWEEN_MOVES)
                service.moveDFS()
            except StopIteration:
                keep_running = False
            m.markDetectedWalls(service.get_environment(), service.get_drone().x, service.get_drone().y)
            screen.blit(m.image(service.get_drone().x, service.get_drone().y), (400, 0))
            pygame.display.flip()

        pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    View.run()
