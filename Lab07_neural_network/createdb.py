import numpy as np

from utils.utils import *
import torch


class Repository:
    @staticmethod
    def createDistribution():
        """
        distribution of 1000 random points in the domain [− 10, 10]^2
        """
        return (MAX_VALUE_DISTRIBUTION_DOMAIN - MIN_VALUE_DISTRIBUTION_DOMAIN) * torch.rand(
            NUMBER_OF_RANDOM_POINTS, NUMBER_OF_PARAMETERS_FOR_FUNCTION
        ) + MIN_VALUE_DISTRIBUTION_DOMAIN  # rand only generates value in [0,1] so we must use the formula to make sure
        # we respect the domain bounds

    @staticmethod
    def computeFunctionValue(pair):
        """
        𝑓(𝑥1, 𝑥2) = 𝑠𝑖𝑛(𝑥1 +𝑥2/π )
        """
        return np.sin((
            pair[0],
            pair[1] / np.pi
        ))

    @staticmethod
    def computeValueAtEachPoint(points):
        """
        the value of the function f for each point
        """
        return torch.tensor(
            [Repository.computeFunctionValue(pointsPair) for pointsPair in points.numpy()]
        )

    @staticmethod
    def createPairs():
        """
        𝑑 𝑖 = ((𝑥1𝑖, 𝑥2𝑖), 𝑓(𝑥1𝑖, 𝑥2𝑖)), 𝑖 = {1,.. 1000}
        """
        initialDistribution = Repository.createDistribution()
        return torch.column_stack((
            initialDistribution,
            Repository.computeValueAtEachPoint(initialDistribution)
        ))

    @staticmethod
    def saveToFile():
        torch.save(
            Repository.createPairs(), FILE_PATH
        )
