import torch
import torch.nn.functional


# declare a class Net that suits your problem (the one from
# example should work if you require just one hidden layer with linear activation
class Net(torch.nn.Module):
    # the class for the network

    def __init__(self, initialLayerSize, hiddenLayerSize, outputLayerSize):
        # we have two layers: a hidden one and an output one
        super(Net, self).__init__()
        self.hiddenLayer = torch.nn.Linear(initialLayerSize, hiddenLayerSize)
        self.outputLayer = torch.nn.Linear(hiddenLayerSize, outputLayerSize)

    def forward(self, data):
        # a function that implements the forward propagation of the signal
        # observe the relu function applied on the output of the hidden layer
        return self.outputLayer(
            torch.nn.functional.relu(self.hiddenLayer(data))
        )
