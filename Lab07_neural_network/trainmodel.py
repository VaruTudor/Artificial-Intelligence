import torch
from myModel import Net
from utils.utils import *
import matplotlib.pyplot


class TrainModel:
    def __init__(self):
        self.lossFunction = torch.nn.MSELoss()
        self.neuralNetwork = Net(INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZE, OUTPUT_LAYER_SIZE).double()
        self.optimizerBatch = torch.optim.SGD(self.neuralNetwork.parameters(), lr=LEARN_SPEED)

        # load the training data data
        pairedTensor = torch.load(FILE_PATH)
        self.inputTensor = pairedTensor.narrow(1, 0, 2)  # just the first 2 columns
        self.outputTensor = pairedTensor.narrow(1, 2, 1)  # just the last column

    def train(self):
        """
        Following the example from file train_Batch.py declare and train your ANN
        """
        lossList = []
        averageLossList = []

        batchCount = int(NUMBER_OF_RANDOM_POINTS / BATCH_SIZE)
        splitInputData = torch.split(self.inputTensor, BATCH_SIZE)
        splitOutputData = torch.split(self.outputTensor, BATCH_SIZE)

        for epoch in range(EPOCH_COUNT):
            lossSum = 0
            for batchIndex in range(batchCount):
                # we compute the output for this batch
                prediction = self.neuralNetwork(splitInputData[batchIndex].double())

                # we compute the loss for this batch
                loss = self.lossFunction(prediction, splitOutputData[batchIndex])

                # we save it for graphics
                lossList.append(loss)

                # we add to the sum for the average list
                lossSum += loss.item()

                # we set up the gradients for the weights to zero (important in pytorch)
                self.optimizerBatch.zero_grad()

                # we compute automatically the variation for each weight (and bias) of the network
                loss.backward()

                # we compute the new values for the weights
                self.optimizerBatch.step()

            averageLossList.append(lossSum / batchCount)

            # we print the loss for all the dataset for each 10th epoch
            if epoch % 100 == 99:
                y_pred = self.neuralNetwork(self.inputTensor.double())
                loss = self.lossFunction(y_pred, self.outputTensor)
                print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

        matplotlib.pyplot.plot(averageLossList)
        matplotlib.pyplot.show()

    def saveToFile(self):
        """
        Save your trained network in file myNetwork.pt
        """
        torch.save(self.neuralNetwork.state_dict(), NETWORK_FILE_PATH)
