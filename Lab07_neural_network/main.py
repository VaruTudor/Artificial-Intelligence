from createdb import Repository
from myModel import Net
from trainmodel import TrainModel
from utils.utils import *


def run():
    x = TrainModel()
    x.train()
    x.saveToFile()

    neuralNetwork = Net(INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZE, OUTPUT_LAYER_SIZE)
    neuralNetwork.load_state_dict(torch.load(NETWORK_FILE_PATH))
    neuralNetwork.eval()

    for inputTensor in INPUT_TENSORS:
        print(neuralNetwork(inputTensor).item())


if __name__ == '__main__':
    # Repository.saveToFile()
    run()
