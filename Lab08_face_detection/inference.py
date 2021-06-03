import random

from matplotlib import pyplot, image
from torchvision import transforms
from train import SimpleNet
from PIL import Image
import torch

from utils.utils import *

IMAGE_PATH_MALE = MEN_FACES_PATH + ' (2).jpg'
IMAGE_PATH_FEMALE = WOMEN_FACES_PATH + ' (1).jpg'
IMAGE_PATH_NON = NON_FACES_PATH + ' (1).jpg'

IMAGE_PATH = IMAGE_PATH_MALE
MODEL_PATH = MODEL_PATH + '_51.model'

IMAGE_SIZE = 32


def read_and_preprocess_image(image_path):
    transformations = transforms.Compose(
        [
            transforms.Resize(IMAGE_SIZE),
            transforms.CenterCrop(IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ]
    )

    return transformations(Image.open(image_path).convert('RGB')).unsqueeze(0)


def process_one_image():
    # load image as pixel array
    data = image.imread(IMAGE_PATH)
    # display the array of pixels as an image
    pyplot.imshow(data)

    model = SimpleNet(num_classes=2)
    model.load_state_dict(torch.load(MODEL_PATH))

    prediction = model(
        read_and_preprocess_image(IMAGE_PATH)
    ).detach().numpy()[0]

    not_face = prediction[0]
    face = prediction[1]

    if face > 0:
        pyplot.text(0, -5, 'Face', fontsize=24)
    elif not_face > 0:
        pyplot.text(0, -5, 'No Face', fontsize=24)
    else:
        print(f"The model cannot determine; raw data: {prediction}")

    pyplot.show()


def choose_random_image_path():
    return random.choice(
        [MEN_FACES_PATH, WOMEN_FACES_PATH, NON_FACES_PATH]
    ) + ' (' + str(random.randint(1, 40)) + ').jpg'


def process_x_images(x: int):
    model = SimpleNet(num_classes=2)
    model.load_state_dict(torch.load(MODEL_PATH))

    for _ in range(x):
        random_path = choose_random_image_path()

        data = image.imread(choose_random_image_path())
        pyplot.imshow(data)

        prediction = model(
            read_and_preprocess_image(random_path)
        ).detach().numpy()[0]

        not_face = prediction[0]
        face = prediction[1]

        if face > 0:
            pyplot.text(0, -5, 'Face', fontsize=24)
        elif not_face > 0:
            pyplot.text(0, -5, 'No Face', fontsize=24)
        else:
            print(f"The model cannot determine; raw data: {prediction}")

        pyplot.show()


if __name__ == '__main__':
    process_one_image()
    # process_x_images(10)
