import queue
import random
from operator import attrgetter

import numpy as np
import pygame

from Assignment4.domain.Ant import Ant
from Assignment4.domain.Sensor import Sensor
from repository import *
from utils import NUMBER_OF_ITERATIONS

DRONE_ENERGY = 0
SENSORS_POSITIONS = [[1, 6], [2, 8], [3, 11], [6, 4]]
NUMBER_OF_ANTS = 3

ALPHA = 0.75
BETA = 2
RHO = 0.5   # used for vaporisation


class controller:
    def __init__(self):
        self.__iterationCount = 1
        self.__map = Map()

        self.__sensors = list()  # sensors are actual nodes
        self.__sensorsPaths = dict()  # paths are actual edges between nodes; cost is the length
        self.__pheromoneForEachPath = dict()
        self.__ants = list()

    """
    We create sensor objects which store both the position of the sensor and the visibility as a list 
    [UP,LEFT,DOWN,RIGHT]
    """
    def determineSensorsVisibility(self):
        for sensor_position in SENSORS_POSITIONS:
            visiblePositions = self.__map.readUDMSensors(sensor_position[0], sensor_position[1])
            self.__sensors.append(
                Sensor(sensor_position, visiblePositions)
            )

    def searchUniformCost(self, startX, startY, finalX, finalY):
        paths = queue.PriorityQueue()
        paths.put((0, [tuple((startX, startY))]))  # we add a list of nodes (path) with priority 0

        while not paths.empty():
            element = paths.get()  # the path with the smallest priority
            path = element[1]
            current = path[len(path) - 1]  # the last node in the path

            if (finalX, finalY) in path:
                return path  # goal reached

            cost = element[0]
            neighbors = self.map.getValidNeighbors(current[0], current[1])  # here we get all possible moves
            for neighbor in neighbors:
                temp = path[:]  # for each neighbor we create an entry in the paths (priority queue)
                temp.append(neighbor)
                paths.put((cost + 1, temp))  # the cost is incremented with 1 (as that is the abstraction for one
                # move in the matrix)

        return list()

    def determineMinimumPathBetweenSensorPairs(self):
        self.determineSensorsVisibility()
        for sensor in self.__sensors:
            for otherSensor in self.__sensors:
                if sensor.position[0] != otherSensor.position[0] and sensor.position[1] != otherSensor.position[1]:
                    self.__sensorsPaths[(sensor, otherSensor)] = self.searchUniformCost(
                        sensor.position[0],
                        sensor.position[1],
                        otherSensor.position[0],
                        otherSensor.position[1]
                    )
                    self.__pheromoneForEachPath[(sensor, otherSensor)] = 1

    def antInitialisation(self):
        self.__ants.clear()
        sensorsCopy = self.__sensors
        for _ in range(NUMBER_OF_ANTS):
            # m ants are randomly placed in n city-nodes (sensors)
            randomSensor = random.choice(sensorsCopy)
            self.__ants.append(Ant(
                randomSensor
            ))
            # sensorsCopy.remove(randomSensor)

    def initialisation(self):
        self.determineMinimumPathBetweenSensorPairs()
        self.antInitialisation()

    def _getAllowedSensorDestinations(self, ant):
        allowedSensors = list()
        for key in self.__sensorsPaths.keys():
            if key[0] == ant.currentSensor and key[1] not in ant.visitedSensors:
                allowedSensors.append(key[1])
        return allowedSensors

    def _totalCostOfPossibleSensorDestinations(self, ant):
        allowedSensors = self._getAllowedSensorDestinations(ant)
        return sum([self.__pheromoneForEachPath[(ant.currentSensor, otherSensor)] ** ALPHA
                    * (1 / len(self.__sensorsPaths[(ant.currentSensor, otherSensor)])) ** BETA for otherSensor in allowedSensors])

    """
    Using the very well-known formula for edge selection (choosing the next sensor to move to) 
    """
    def chooseNextSensor(self, ant):
        allowedSensors = self._getAllowedSensorDestinations(ant)
        if not len(allowedSensors):
            # there is no other sensor destination
            return 0

        probabilitiesForPossibleNextSensors = list()
        for sensor in allowedSensors:
            # compute the probability and add them to a list for a weighted random choice
            pheromoneIntensity = self.__pheromoneForEachPath[(ant.currentSensor, sensor)]
            visibility = 1 / len(self.__sensorsPaths[(ant.currentSensor, sensor)])  # larger distance -> worse visibility
            totalSum = self._totalCostOfPossibleSensorDestinations(ant)
            probabilitiesForPossibleNextSensors.append(pheromoneIntensity ** ALPHA * visibility ** BETA / totalSum)

        # we return a next sensor (computed with probability)
        return np.random.choice(allowedSensors, 1, p=probabilitiesForPossibleNextSensors).item(0)

    def iterate(self):
        stillGoing = True
        while stillGoing:
            for ant in self.__ants:
                # choose a next sensor for each ant
                nextSensor = self.chooseNextSensor(ant)
                ant.addSensorToVisited(nextSensor)

                # change locally the pheromone trail with evaporation
                current = (1-RHO) * (1 / len(self.__sensorsPaths[(ant.currentSensor, nextSensor)]))
                older = RHO * self.__pheromoneForEachPath[(ant.currentSensor, nextSensor)]
                ant.localPheromones[(ant.currentSensor, nextSensor)] = current + older
                ant.totalPheromone += current + older

                # change the current sensor in ant
                ant.currentSensor = nextSensor
                if len(ant.visitedSensors) == len(self.__sensors):
                    stillGoing = False

    def updatePheromones(self):
        for edge in self.__sensorsPaths.keys():
            totalPheromoneForEdge = 0
            for ant in self.__ants:
                try:
                    totalPheromoneForEdge += ant.localPheromones[edge] / len(self.__sensorsPaths[edge])
                except KeyError:
                    continue

            # compute the intensity of pheromone trail with evaporation
            self.__pheromoneForEachPath[edge] = (1-RHO) * self.__pheromoneForEachPath[edge] + totalPheromoneForEdge

    def run(self):
        for _ in range(NUMBER_OF_ITERATIONS):
            self.initialisation()
            self.iterate()
            self.updatePheromones()

            bestAnt = max(self.__ants, key=attrgetter('totalPheromone'))
            finalPath = list()

            for edge in bestAnt.localPheromones.keys():
                for step in self.__sensorsPaths[edge]:
                    finalPath.append(step)

            return list(dict.fromkeys(finalPath))

    def powerSensors(self):
        for sensor in self.__sensors:
            sensor.updateEnergy(min(sensor.visiblePositions))

    @staticmethod
    def mapWithDrone(mapImage):
        drone = pygame.image.load("utils/drona.png")
        mapImage.blit(drone, (0, 0))
        return mapImage

    @property
    def map(self):
        return self.__map
