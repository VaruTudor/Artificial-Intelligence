import numpy as np
import torch

MIN_VALUE_DISTRIBUTION_DOMAIN = -10
MAX_VALUE_DISTRIBUTION_DOMAIN = 10
NUMBER_OF_RANDOM_POINTS = 1000
NUMBER_OF_PARAMETERS_FOR_FUNCTION = 2

FILE_PATH = 'utils/mydataset.dat'
NETWORK_FILE_PATH = 'utils/myNetwork.pt'

BATCH_SIZE = 20
EPOCH_COUNT = 5000
LEARN_SPEED = 0.01

INPUT_LAYER_SIZE = 2
HIDDEN_LAYER_SIZE = 10
OUTPUT_LAYER_SIZE = 1


INPUT_TENSORS = [
    torch.tensor([0.0, 1.0]),
    torch.tensor([1.0, 0.0]),
    torch.tensor([-3.0, 3.0]),
    torch.tensor([1.0, 1.0]),
    torch.tensor([2.0, 2.0]),
    torch.tensor([np.pi, np.pi]),
    torch.tensor([np.pi, 0]),
    torch.tensor([0, np.pi]),
]