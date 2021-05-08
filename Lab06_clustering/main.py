# K-means algorithm

# If val1 would be much larger than val2 (or reverse) we would need to perform some scaling

# from sklearn.cluster import KMeans
from kMeans import KMeans
import pandas as pd
from matplotlib import pyplot as plt

from statistics import computeAccuracy, computePrecision, computeRappel, computeScore
from utils import K, FILE_NAME, MAX_K, COLORS, NUMBER_DECIMAL_DIGITS

# read the data from the file
data = pd.read_csv(FILE_NAME)

# create a KMeans object with K clusters
kMeans = KMeans(n_clusters=K)
# compute cluster centers (centroids) and predict cluster index for each sample
outputFitPredict = kMeans.fit_predict(data[['val1', 'val2']])

centroids = kMeans.cluster_centers_


def initialPlot():
    plt.scatter(data['val1'], data['val2'])
    plt.show()


def firstClusteringPlot():
    data['cluster'] = outputFitPredict
    for clusterValue in range(K):
        # group data into K containers based on each cluster
        dataHavingClusterValue = data[data.cluster == clusterValue]
        # scatter them with different colors
        plt.scatter(dataHavingClusterValue['val1'],
                    dataHavingClusterValue['val2'],
                    color=COLORS[clusterValue],
                    label='Cluster ' + str(clusterValue))

    # scatter the centroids
    plt.scatter(centroids[:, 0], centroids[:, 1],
                color='purple',
                marker='*',
                label='centroid')

    # set axes labels
    plt.xlabel('val1')
    plt.ylabel('val2')
    plt.show()


def elbowPlot():
    K_Range = range(1, MAX_K)
    sumSquaredErrors = []
    for k in K_Range:
        # we do the algorithm for each possible k
        possibleKMeanValue = KMeans(n_clusters=k)
        possibleKMeanValue.fit(data[['val1', 'val2']])
        sumSquaredErrors.append(possibleKMeanValue.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of squared error')
    plt.plot(K_Range, sumSquaredErrors)
    plt.show()


def printAnalysis():
    # we use this to associate correctly cluster(which are ints) to initial labels
    # assuming some values are correct as cluster number might change at run-time
    # (1 might represent A one time and B another, so the check must be performed after run-time)
    CONVERT_TO_NUMBERS = {
        outputFitPredict[len(outputFitPredict) - 1]: 'A',
        outputFitPredict[3]: 'B',
        outputFitPredict[len(outputFitPredict) - 2]: 'C',
        outputFitPredict[1]: 'D'
    }

    # data from file
    predictedResult = data['label']

    # computed data
    actualResult = []
    for element in outputFitPredict:
        actualResult.append(
            CONVERT_TO_NUMBERS[element]
        )

    accuracy = computeAccuracy(predictedResult, actualResult)
    print('Number of matching labels: ' + str(accuracy[0]))
    print('Accuracy: ' + str(accuracy[1]))
    print('Precision: ' + str(round(computePrecision(predictedResult, actualResult), NUMBER_DECIMAL_DIGITS)))
    print('Rappel: ' + str(round(computeRappel(predictedResult, actualResult), NUMBER_DECIMAL_DIGITS)))
    print('Score: ' + str(round(computeScore(predictedResult, actualResult), NUMBER_DECIMAL_DIGITS)))


def run():
    if K > MAX_K:
        print('need more colors')
    # plot of initial data
    initialPlot()

    # plot of initial clustering
    firstClusteringPlot()

    # plot the 'elbow' to see the best value for K
    elbowPlot()

    # show accuracy
    printAnalysis()


if __name__ == '__main__':
    run()
