# -*- coding: utf-8 -*-

from random import randint

from Assignment4.domain.Map import Map

LAST_POPULATION = -1
DUMMY_STARTING_POSITION = 0  # will be changed later by a setter

# TODO 1. u need to store distances and pheromone levels in two different structures
#  2. simplify the structure (maybe remove the repo) and add classes maybe for ants
#  3. follow the steps from the slides and watch other videos if needed


class repository:
    def __init__(self):
        self.__populations = []

        self.__drone = [DUMMY_STARTING_POSITION, DUMMY_STARTING_POSITION]

    def setDroneInitialPosition(self, newPosition):
        self.__drone = newPosition

    def getCurrentPopulation(self):
        return self.__populations[LAST_POPULATION]

    def random_drone(self):
        x = randint(0, self.__map.n - 1)
        y = randint(0, self.__map.m - 1)
        while self.__map.surface[x][y] != 0:
            x = randint(0, self.__map.n - 1)
            y = randint(0, self.__map.m - 1)
        self.__drone = [x, y]

    def addPopulation(self, population):
        self.__populations.append(population)

    def getBestPath(self):
        return self.__populations[LAST_POPULATION].getBestPath()

    @staticmethod
    def addIndividual(population, individual):
        population.addIndividual(individual)



    @property
    def drone(self):
        return self.__drone
