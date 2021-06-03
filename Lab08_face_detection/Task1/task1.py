from PIL import Image

from matplotlib import image
from matplotlib import pyplot

IMAGE_PATH = './utils/f1.jpg'
RESIZE_TO = (100, 100)


def display_image_with_pillow():
    # load the image
    image = Image.open(IMAGE_PATH)

    # summarize some details about the image
    print(image.format)
    print(image.mode)
    print(image.size)

    # show the image
    image.show()


def convert_image_to_numpy_array():
    # load image as pixel array
    data = image.imread(IMAGE_PATH)

    # summarize shape of the pixel array
    print(data.dtype)
    print(data.shape)

    # display the array of pixels as an image
    pyplot.imshow(data)
    pyplot.show()


def resize_image_to_specific_dimensions():
    # load the image
    image = Image.open(IMAGE_PATH)

    # report the size of the image
    print(image.size)

    # create a thumbnail and preserve aspect ratio
    image.thumbnail(RESIZE_TO)

    # report the size of the thumbnail
    print(image.size)


def task1():
    display_image_with_pillow()
    convert_image_to_numpy_array()
    resize_image_to_specific_dimensions()
