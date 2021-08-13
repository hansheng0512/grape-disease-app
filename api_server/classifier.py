import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F
from api_server.config import CLASSES, NUM_CLASSES, MODEL_WEIGHT_PATH, TRANSFORM

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5)
        self.relu1 = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.relu2 = nn.ReLU()
        # Note that the input of this layers is depending on your input image sizes
        self.fc1 = nn.Linear(in_features=34*34*16, out_features=120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, NUM_CLASSES)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu1(self.conv1(x)))
        x = self.pool(self.relu2(self.conv2(x)))
        x = torch.flatten(x, 1)  # Flatten all dimensions except batch
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class SqueezeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = Net()
        print(MODEL_WEIGHT_PATH)
        self.model.load_state_dict(
            torch.load(MODEL_WEIGHT_PATH, map_location=torch.device("cpu"))
        )

    def predict(self, image):
        image = TRANSFORM(image)
        image = image.unsqueeze(0)
        output = self.model(image)
        class_index = torch.argmax(output, dim=1)

        return CLASSES[class_index]


if __name__ == "__main__":
    model = SqueezeNet()
    print(model)
