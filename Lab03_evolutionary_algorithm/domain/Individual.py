import copy
from random import *

import numpy as np

from Assignment3.utils import UP, DOWN, LEFT, RIGHT
import secrets

POSSIBLE_GENE_VALUES = [UP, RIGHT, DOWN, LEFT]
START_STUCK = 1   # negative number, so that we don't mistake it for a bad path
BORDER_STUCK = 0   # negative number, so that we don't mistake it for a bad path
# using it we check if we start on a valid square
MAP_TERRITORY = [element for element in range(0, 20)]


class Gene:
    def __init__(self):
        self.value = secrets.choice(
            POSSIBLE_GENE_VALUES    # we chose a random value from UP/DOWN/LEFT/RIGHT
        )

    @staticmethod
    def getNewGeneWithValue(value):
        gene = Gene()
        gene.value = value
        return gene

    def __str__(self):
        return "Gene->" + str(self.value)

    def __repr__(self):
        return "Gene->" + str(self.value)


class Individual:
    def __init__(self, mapCopy, dronePosition, size=0):
        self.__size = size
        self.__path = [Gene() for _ in range(self.__size)]
        self.__mapCopy = mapCopy
        self.__dronePosition = dronePosition
        self.__f = self.fitness()

    def newVerticalPositions(self):
        allNewVisiblePosition = self.__mapCopy.readUDMSensors(
            self.__dronePosition[0],
            self.__dronePosition[1])

        return allNewVisiblePosition[UP] + allNewVisiblePosition[DOWN]

    def newHorizontalPositions(self):
        allNewVisiblePosition = self.__mapCopy.readUDMSensors(
            self.__dronePosition[0],
            self.__dronePosition[1])

        return allNewVisiblePosition[LEFT] + allNewVisiblePosition[RIGHT]

    def checkMapConstraint(self, givenPosition):
        if givenPosition[0] in MAP_TERRITORY and givenPosition[1] in MAP_TERRITORY:
            return True
        return False

    def fitness(self):
        wentOverWall = 0
        if not self.checkMapConstraint(self.__dronePosition):
            return BORDER_STUCK
        if self.__mapCopy.surface[self.__dronePosition[0]][self.__dronePosition[1]] == 1:
            return START_STUCK   # if first position is a wall
        finalFitness = sum(self.__mapCopy.readUDMSensors(
            self.__dronePosition[0],
            self.__dronePosition[1]
        ))  # put all visible positions from the initial position of the drone

        currentPosition = copy.deepcopy(self.__dronePosition)

        localPath = list()
        localPath.append(copy.deepcopy(currentPosition))
        for position in self.__path:

            if self.__mapCopy.surface[currentPosition[0]][currentPosition[1]] == 1:
                wentOverWall += 1  # when finding a wall
                # the reason we don't block the path is to not get stuck in a local optima after that
                # we only add the new visible positions (if we advance vertically, no new vertical positions will
                # appear)
            elif position.value == UP:
                currentPosition[0] = currentPosition[0] - 1
                if not self.checkMapConstraint(currentPosition):
                    return BORDER_STUCK

                if currentPosition not in localPath:
                    finalFitness += self.newHorizontalPositions()
                localPath.append(copy.deepcopy(currentPosition))

            elif position.value == DOWN:
                currentPosition[0] = currentPosition[0] + 1
                if not self.checkMapConstraint(currentPosition):
                    return BORDER_STUCK

                if currentPosition not in localPath:
                    finalFitness += self.newHorizontalPositions()
                localPath.append(copy.deepcopy(currentPosition))

            elif position.value == LEFT:
                currentPosition[1] = currentPosition[1] - 1
                if not self.checkMapConstraint(currentPosition):
                    return BORDER_STUCK

                if currentPosition not in localPath:
                    finalFitness += self.newVerticalPositions()
                localPath.append(copy.deepcopy(currentPosition))

            elif position.value == RIGHT:
                currentPosition[1] = currentPosition[1] + 1
                if not self.checkMapConstraint(currentPosition):
                    return BORDER_STUCK

                if currentPosition not in localPath:
                    finalFitness += self.newVerticalPositions()
                localPath.append(copy.deepcopy(currentPosition))

        if wentOverWall:
            finalFitness = int(finalFitness/(2 ** wentOverWall))
        return finalFitness

    def mutate(self, mutateProbability=0.04):
        # performing a creep mutation
        if random() < mutateProbability:
            randomGeneIndex = randint(0, self.__size-1)     # randomly select a position from the representation
            geneValuesForMutation = copy.deepcopy(POSSIBLE_GENE_VALUES)    # take the possible gene values
            geneValuesForMutation.remove(self.__path[randomGeneIndex].value)     # keep only values that differ from the one
            # we want to change

            self.__path[randomGeneIndex] = Gene.getNewGeneWithValue(
                np.random.choice(geneValuesForMutation)
            )  # change the value randomly with one from the above selected

    def crossover(self, otherParent, crossoverProbability=0.8):
        # here we use cutting points
        offspring1, offspring2 = Individual(self.__mapCopy, self.__dronePosition, self.__size),\
                                 Individual(self.__mapCopy, self.__dronePosition, self.__size)

        if random() < crossoverProbability:
            randomGeneIndex = randint(0, self.__size-1)     # randomly select a position from the representation used
            # as a cutting point
            offspring1.__path = self.__path[:randomGeneIndex] + otherParent.__path[randomGeneIndex:]
            offspring2.__path = otherParent.__path[:randomGeneIndex] + self.__path[randomGeneIndex:]

        return offspring1, offspring2

    def computePath(self):
        finalX = self.__dronePosition[0]
        finalY = self.__dronePosition[1]
        path = [[finalY, finalX]]
        # iterate reversely in positions
        pathTaken = copy.deepcopy(self.__path)
        pathTaken.reverse()
        for position in pathTaken:
            if position.value == UP:
                finalY += 1
                path.append([finalY, finalX])
            elif position.value == DOWN:
                finalY -= 1
                path.append([finalY, finalX])
            elif position.value == LEFT:
                finalX += 1
                path.append([finalY, finalX])
            elif position.value == RIGHT:
                finalX -= 1
                path.append([finalY, finalX])
        return path

    def getFitness(self):
        return self.__f
