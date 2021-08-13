import torchvision.transforms as transforms
import os

NORMALIZE = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

TRANSFORM = transforms.Compose(
    [
        transforms.Resize(150),
        transforms.CenterCrop(150),
        transforms.ToTensor(),
    ]
)

NUM_CLASSES = 4
CLASSES = ['Black Rot', 'Esca (Black_Measles)', 'Leaf Blight (Isariopsis Leaf Spot)', 'Healthy']
FILENAME = "grape_disease_state_dict.pt"
FILE_PATH = os.path.realpath(__file__)
MODEL_WEIGHT_PATH = os.path.join(os.path.dirname(FILE_PATH), "model", FILENAME)
