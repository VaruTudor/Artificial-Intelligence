import random
import time

import numpy as np
import pygame

from repository import *
POPULATION_SIZE = 100
SELECTION_SIZE = POPULATION_SIZE - 2
INDIVIDUAL_SIZE = 10
CROSSOVER_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.2
NUMBER_OF_ITERATIONS = 100
NUMBER_OF_SEEDS = 2


class controller:
    def __init__(self, givenRepository: repository):
        self.__repository = givenRepository
        self.__statistics = list()
        self.__iterationCount = 1

    def setDroneInitialPosition(self, newPosition):
        self.__repository.setDroneInitialPosition(newPosition)

    def iteration(self):
        self.__iterationCount += 1

        population = self.__repository.getCurrentPopulation()
        selectedIndividuals = population.selection(SELECTION_SIZE)  # selection of the parrents
        parents = selectedIndividuals[:len(selectedIndividuals) // 2]    # using // to do a floor division
        pairsOfParentsNeeded = len(parents) // 2
        parentPairsUsed = list()
        for _ in range(pairsOfParentsNeeded):
            firstParent = random.choice(parents)
            secondParent = random.choice(parents)
            if (firstParent, secondParent) not in parentPairsUsed:
                parentPairsUsed.append((firstParent, secondParent))
                # create offsprings by crossover of the parents
                firstChild, secondChild = firstParent.crossover(secondParent, CROSSOVER_PROBABILITY)
                firstChild.mutate(MUTATION_PROBABILITY)  # apply some mutations
                secondChild.mutate(MUTATION_PROBABILITY)
                repository.addIndividual(population, firstChild)
                repository.addIndividual(population, secondChild)
        population.v = selectedIndividuals.tolist()  # transform from ndarray to list

    def run(self):
        # until stop condition
        for _ in range(NUMBER_OF_ITERATIONS):
            self.iteration()    # perform an iteration
            average, std = self.__repository.getAverageAndStdOfLastPopulation()
            self.__statistics.append([np.average(average), np.std(average)])    # save the information

    def solver(self):
        for i in range(NUMBER_OF_SEEDS):
            random.seed(i)
            population = self.__repository.createPopulation(POPULATION_SIZE, INDIVIDUAL_SIZE)  # create the population
            self.__repository.addPopulation(population)
            self.run()  # run the algorithm
        # return the results and the statistics
        return self.__repository.getBestPath(), self.__statistics

    @staticmethod
    def mapWithDrone(mapImage):
        drone = pygame.image.load("utils/drona.png")
        mapImage.blit(drone, (0, 0))
        return mapImage
