import pygame
from pygame.locals import *

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3


class Service:
    def __init__(self, drone, environment):
        self.__drone = drone
        self.__environment = environment
        self.visitedStack = list()
        self.tracebackStack = list()

    def get_drone(self): return self.__drone
    def get_environment(self): return self.__environment

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.__drone.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.__drone.x-1][self.__drone.y] == 0:
                self.__drone.x = self.__drone.x - 1
        if self.__drone.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.__drone.x+1][self.__drone.y] == 0:
                self.__drone.x = self.__drone.x + 1

        if self.__drone.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.__drone.x][self.__drone.y-1] == 0:
                self.__drone.y = self.__drone.y - 1
        if self.__drone.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.__drone.x][self.__drone.y+1] == 0:
                self.__drone.y = self.__drone.y + 1

    def moveDFS(self):
        # we pause the execution for .1 of a second each iteration

        walls = self.__environment.readUDMSensors(self.__drone.x, self.__drone.y)

        if walls[UP] > 0 and not self.visitedStack.__contains__([self.__drone.x-1, self.__drone.y]):
            # if there are no walls UP we go there and visit
            self.__drone.x = self.__drone.x - 1
            self.visitedStack.append([self.__drone.x, self.__drone.y])
            self.tracebackStack.append([self.__drone.x, self.__drone.y])
        elif walls[1] > 0 and not self.visitedStack.__contains__([self.__drone.x, self.__drone.y+1]):
            # if there are no walls RIGHT we go there and visit
            self.__drone.y = self.__drone.y + 1
            self.visitedStack.append([self.__drone.x, self.__drone.y])
            self.tracebackStack.append([self.__drone.x, self.__drone.y])
        elif walls[DOWN] > 0 and not self.visitedStack.__contains__([self.__drone.x+1, self.__drone.y]):
            # if there are no walls DOWN we go there and visit
            self.__drone.x = self.__drone.x + 1
            self.visitedStack.append([self.__drone.x, self.__drone.y])
            self.tracebackStack.append([self.__drone.x, self.__drone.y])
        elif walls[3] > 0 and not self.visitedStack.__contains__([self.__drone.x, self.__drone.y-1]):
            # if there are no walls LEFT we go there and visit
            self.__drone.y = self.__drone.y - 1
            self.visitedStack.append([self.__drone.x, self.__drone.y])
            self.tracebackStack.append([self.__drone.x, self.__drone.y])
        else:
            # in this case we cannot visit any adjacent node(position in map)
            # we have to trace back to an element which can move to a non visited vertex
            try:
                tracebackPosition = self.tracebackStack.pop(len(self.tracebackStack)-1)
                if tracebackPosition[0] == self.__drone.x and tracebackPosition[1] == self.__drone.y:
                    # we perform another pop if the element we popped first time is the current position
                    tracebackPosition = self.tracebackStack.pop(len(self.tracebackStack)-1)
                self.__drone.x = tracebackPosition[0]
                self.__drone.y = tracebackPosition[1]
            except IndexError:
                print("DFS complete!")
                raise StopIteration
