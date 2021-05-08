from sklearn.metrics import accuracy_score


def computeAccuracy(predictedResult, actualResult):
    return accuracy_score(predictedResult, actualResult, normalize=False), accuracy_score(predictedResult, actualResult)


def computeConfusionMatrix(predictedResult, actualResult):
    confusionMatrix = {'A': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
                       'B': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
                       'C': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
                       'D': {'A': 0, 'B': 0, 'C': 0, 'D': 0}}

    # populate matrix as accuracy would be one (same labels as predicted)
    for predictedResultElement in predictedResult:
        confusionMatrix[predictedResultElement][predictedResultElement] += 1

    for index in range(len(predictedResult)):
        # when result does not meet predicted labels
        if predictedResult[index] != actualResult[index]:
            # decrease for the predicted match
            confusionMatrix[predictedResult[index]][predictedResult[index]] -= 1
            # increase for the actual match
            confusionMatrix[predictedResult[index]][actualResult[index]] += 1

    return confusionMatrix


def computeFalsePositive(predictedResult, actualResult):
    falsePositive = 0
    confusionMatrix = computeConfusionMatrix(predictedResult, actualResult)

    for cluster in confusionMatrix.values():
        for clusterMatch in cluster.keys():
            for otherClusterMatch in cluster.keys():
                # not counting pairs with identical elements (diagonal)
                if clusterMatch != otherClusterMatch:
                    # count the pair for different elements
                    # pairs will be counted twice
                    falsePositive += cluster[clusterMatch] * cluster[otherClusterMatch]

    # we counted twice
    falsePositive //= 2

    return falsePositive


def computeFalseNegative(predictedResult, actualResult):
    falseNegative = 0
    confusionMatrix = computeConfusionMatrix(predictedResult, actualResult)

    for clusterName in confusionMatrix.keys():
        cluster = confusionMatrix.values()
        for clusterMatch in cluster:
            for otherClusterMatch in cluster:
                if clusterMatch != otherClusterMatch:
                    # pairs will be counted twice
                    falseNegative += clusterMatch[clusterName] * otherClusterMatch[clusterName]

    # we counted twice
    falseNegative //= 2

    return falseNegative


def computeTruePositive(predictedResult, actualResult):
    truePositive = 0
    confusionMatrix = computeConfusionMatrix(predictedResult, actualResult)

    for cluster in confusionMatrix.values():
        for valuePerClusterMatch in cluster.values():
            # count all pairs using formula
            truePositive += (valuePerClusterMatch * (valuePerClusterMatch - 1)) // 2

    return truePositive


# TP/(TP+FP)
def computePrecision(predictedResult, actualResult):
    falsePositive = computeFalsePositive(predictedResult, actualResult)
    truePositive = computeTruePositive(predictedResult, actualResult)
    return truePositive / (truePositive + falsePositive)


# TP/(TP+FN)
def computeRappel(predictedResult, actualResult):
    falseNegative = computeFalseNegative(predictedResult, actualResult)
    truePositive = computeTruePositive(predictedResult, actualResult)
    return truePositive / (truePositive + falseNegative)


# 2PR/(P+R)
def computeScore(predictedResult, actualResult):
    rappel = computeRappel(predictedResult, actualResult)
    precision = computePrecision(predictedResult, actualResult)
    return 2 * rappel * precision / (rappel + precision)
