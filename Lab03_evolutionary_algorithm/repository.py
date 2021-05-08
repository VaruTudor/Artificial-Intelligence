# -*- coding: utf-8 -*-

from random import randint

from Assignment3.domain.Map import Map
from Assignment3.domain.Population import Population

LAST_POPULATION = -1
DUMMY_STARTING_POSITION = 0  # will be changed later by a setter


class repository:
    def __init__(self):
        self.__populations = []
        self.__map = Map()
        self.__drone = [DUMMY_STARTING_POSITION, DUMMY_STARTING_POSITION]

    def createPopulation(self, populationSize, individualSize):
        return Population(self.__map, self.__drone, populationSize, individualSize)

    def getAverageAndStdOfLastPopulation(self):
        return self.__populations[LAST_POPULATION].findAverageAndStd()

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
    def map(self):
        return self.__map

    @property
    def drone(self):
        return self.__drone
