import torch.nn as nn
from torch.autograd import Variable
from torch.optim import Adam
from torch.utils.data import DataLoader

from load_data import *

Image.MAX_IMAGE_PIXELS = None


class Unit(nn.Module):
    """
    Similar to the example given in the lab requirement.
    """
    def __init__(self, in_channels, out_channels):
        super(Unit, self).__init__()

        self.conv = nn.Conv2d(in_channels=in_channels, kernel_size=3, out_channels=out_channels, stride=1, padding=1)
        self.bn = nn.BatchNorm2d(num_features=out_channels)
        self.relu = nn.ReLU()

    def forward(self, input_data):
        output = self.conv(input_data)
        output = self.bn(output)
        output = self.relu(output)

        return output


class SimpleNet(nn.Module):
    """
    Similar to the example given in the lab requirement.
    """
    def __init__(self, num_classes=2):
        super(SimpleNet, self).__init__()

        # Create 14 layers of the unit with max pooling in between
        self.unit1 = Unit(in_channels=3, out_channels=32)
        self.unit2 = Unit(in_channels=32, out_channels=32)
        self.unit3 = Unit(in_channels=32, out_channels=32)

        self.pool1 = nn.MaxPool2d(kernel_size=2)

        self.unit4 = Unit(in_channels=32, out_channels=64)
        self.unit5 = Unit(in_channels=64, out_channels=64)
        self.unit6 = Unit(in_channels=64, out_channels=64)
        self.unit7 = Unit(in_channels=64, out_channels=64)

        self.pool2 = nn.MaxPool2d(kernel_size=2)

        self.unit8 = Unit(in_channels=64, out_channels=128)
        self.unit9 = Unit(in_channels=128, out_channels=128)
        self.unit10 = Unit(in_channels=128, out_channels=128)
        self.unit11 = Unit(in_channels=128, out_channels=128)

        self.pool3 = nn.MaxPool2d(kernel_size=2)

        self.unit12 = Unit(in_channels=128, out_channels=128)
        self.unit13 = Unit(in_channels=128, out_channels=128)
        self.unit14 = Unit(in_channels=128, out_channels=128)

        self.avg_pool = nn.AvgPool2d(kernel_size=4)

        # Add all units into the Sequential layer in the same order
        self.net = nn.Sequential(
            self.unit1,
            self.unit2,
            self.unit3,
            self.pool1,
            self.unit4,
            self.unit5,
            self.unit6,
            self.unit7,
            self.pool2,
            self.unit8,
            self.unit9,
            self.unit10,
            self.unit11,
            self.pool3,
            self.unit12,
            self.unit13,
            self.unit14,
            self.avg_pool
        )

        self.fc = nn.Linear(in_features=128, out_features=num_classes)

    def forward(self, input_data):
        output = self.net(input_data)
        output = output.view(-1, 128)
        output = self.fc(output)
        return output


def adjust_learning_rate(optimizer, epoch):
    """
    learning rate adjustment that divides the learning rate by 10 every 30 epochs
    """
    lr = 0.0001

    if epoch > 180:
        lr = lr / 1000000
    elif epoch > 150:
        lr = lr / 100000
    elif epoch > 120:
        lr = lr / 10000
    elif epoch > 90:
        lr = lr / 1000
    elif epoch > 60:
        lr = lr / 100
    elif epoch > 30:
        lr = lr / 10

    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


def save_models(model, epoch):
    torch.save(model.state_dict(),
               "C:/Users/Tudor/Desktop/D/faculta/SemIV/AI/Labs/Lab08_face_detection/utils/models/model_{}.model".format(
                   epoch))
    print("Checkpoint saved")


def test(model, test_loader):
    model.eval()
    test_acc = 0.0

    for _, (images, labels) in enumerate(test_loader):

        if torch.cuda.is_available():
            images = Variable(images.cuda())
            labels = Variable(labels.cuda())

        # Predict classes using image from the test set
        outputs = model(images)

        _, prediction = torch.max(outputs.data, 1)

        test_acc += torch.sum(torch.eq(prediction, labels.data))

    # Compute the average acc and loss over all 10000 test images
    test_acc = test_acc / len(test_loader)

    return test_acc


def train(model, optimizer, loss_fn, train_loader, test_loader, num_epochs):
    best_acc = 0.0

    for epoch in range(num_epochs):
        model.train()

        train_acc = 0.0
        train_loss = 0.0

        for _, (images, labels) in enumerate(train_loader):

            if torch.cuda.is_available():
                images = Variable(images.cuda())
                labels = Variable(labels.cuda())

            # Clear all accumulated gradients
            optimizer.zero_grad()
            # Predict classes using images from the test set
            outputs = model(images)
            # Compute the loss based on the predictions and actual labels
            loss = loss_fn(outputs, labels)
            # Propagate the loss backwards
            loss.backward()

            optimizer.step()

            train_loss += loss.cpu().data.item() * images.size(0)
            _, prediction = torch.max(outputs.data, 1)

            train_acc += torch.sum(prediction == labels.data)

        adjust_learning_rate(optimizer, epoch)

        train_acc = train_acc / len(train_loader)
        train_loss = train_loss / len(train_loader)

        test_acc = test(model, test_loader)

        print("Epoch {}: Train Accuracy: {:.4f}, TrainLoss: {:.4f}, Test Accuracy: {:.4f}".format(epoch, train_acc,
                                                                                                  train_loss, test_acc))

        if test_acc >= best_acc:
            save_models(model, epoch)
            best_acc = test_acc


if __name__ == "__main__":
    train_set, test_set = get_data_set()
    batch_size = 1

    # Create a loader for the training set
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=4)
    # Create a loader for the testing set
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=4)
    # Create the model
    model = SimpleNet(num_classes=2)
    # Check if gpu support is available
    if torch.cuda.is_available():
        model.cuda()
    # Create the model optimizer
    optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
    # Create the model loss function
    loss_fn = nn.CrossEntropyLoss()

    train(model, optimizer, loss_fn, train_loader, test_loader, 300)
