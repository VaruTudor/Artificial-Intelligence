import time

import pygame

from controller import SENSORS_POSITIONS
from utils import BLUE, WHITE, RED
TIME_BETWEEN_MOVES = 0.5


class UI:
    def __init__(self, newController):
        self._controller = newController
        self._path = []
        self._stats = []
        self._iterations = []

    @staticmethod
    def moveDrona(mapImage, x, y):
        drona = pygame.image.load("utils/drona.png")
        mapImage.blit(drona, (y * 20, x * 20))
        return mapImage

    def image(self):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(20):
            for j in range(20):
                if self._controller.map.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
        sensorBrick = pygame.Surface((20, 20))
        sensorBrick.fill(RED)
        for sensorPosition in SENSORS_POSITIONS:
            imagine.blit(sensorBrick, (sensorPosition[1] * 20, sensorPosition[0] * 20))

        return imagine

    def run(self):
        self._controller.map.loadMap("utils/test2.map")

        pygame.init()
        # load and set the logo
        logo = pygame.image.load("utils/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        startTime = time.time()
        self._path = self._controller.run()
        print("\n ACO path   " + self._path.__str__() +
              "\n ACO path-find  : %s seconds\n" % (time.time() - startTime))

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)

        # define a variable to control the main loop
        running = True

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            if self._path.__len__() > 0:
                dronePosition = self._path.pop(0)
                time.sleep(TIME_BETWEEN_MOVES)

                screen.blit((self.moveDrona(self.image(), dronePosition[0], dronePosition[1])), (0, 0))
                pygame.display.flip()

        pygame.quit()
