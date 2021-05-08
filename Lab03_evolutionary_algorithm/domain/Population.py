import copy

import numpy as np

from Assignment3.domain.Individual import Individual


class Population:
    def __init__(self, mapCopy, droneInitialPosition, populationSize=0, individualSize=0):
        self.__populationSize = populationSize
        self.__v = [Individual(mapCopy, copy.deepcopy(droneInitialPosition), individualSize) for _ in range(populationSize)]

    def addIndividual(self, individual):
        self.__v.append(individual)

    def evaluate(self):
        # evaluates the population
        for x in self.__v:
            x.fitness()

    @staticmethod
    def computeProbability(individualFitness, sumFitness):
        return individualFitness / sumFitness

    """
        For the selection we use a uniform distribution in order to not get stuck in a local optima
        (even individuals with lower fitness get a chance and by repetition we make sure we don't remove a "weaker"
        individual which can lead in the future to the global optima) 
    """
    def selection(self, k=0):
        sumFitness = sum([individual.getFitness() for individual in self.__v])
        probabilityForEachIndividual = [self.computeProbability(individual.getFitness(), sumFitness) for individual in
                                        self.__v]
        # here we store the probability (with symmetric position with self.__v)
        copyOfIndividuals = self.__v.copy()

        return np.random.choice(copyOfIndividuals, k, p=probabilityForEachIndividual)
        # perform a selection of k individuals from the population using Monte Carlo
        # and returns that selection

    def findAverageAndStd(self):
        totalFitness = list()
        for individual in self.__v:
            totalFitness.append(individual.getFitness())
        return np.average(totalFitness), np.std(totalFitness)

    def getBestPath(self):
        return max(self.__v, key=lambda individual: individual.getFitness()).computePath()

    @property
    def v(self):
        return self.__v

    @v.setter
    def v(self, other):
        self.__v = other
