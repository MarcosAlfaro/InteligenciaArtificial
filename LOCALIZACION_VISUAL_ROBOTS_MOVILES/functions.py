"""
This script includes several functions that are often used by the other scripts
"""

import torch
import os
from PIL import Image
from sklearn.neighbors import KDTree
from config import PARAMS

device = torch.device(PARAMS.device if torch.cuda.is_available() else 'cpu')


def create_path(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return directory


def get_coords(imageDir):
    idxX, idxY, idxA = imageDir.index('_x'), imageDir.index('_y'), imageDir.index('_a')
    x, y = float(imageDir[idxX + 2:idxY]), float(imageDir[idxY + 2:idxA])
    return x, y


def get_env(env):
    if env == "SA_B":
        environment = "SAARBRUCKEN_B"
    elif env == "SA_A":
        environment = "SAARBRUCKEN_A"
    elif env == "FR_B":
        environment = "FRIBURGO_B"
    elif env == "FR_A":
        environment = "FRIBURGO_A"
    else:
        raise ValueError("Environment not available. Valid environments: FR_A, FR_B, SA_A, SA_B")
    return environment


def get_cond_ilum(env):
    if env in ["FR_A", "SA_B"]:
        condIlum = ['Cloudy', 'Night', 'Sunny']
    elif env == "FR_B":
        condIlum = ['Cloudy', 'Sunny']
    elif env == "SA_A":
        condIlum = ['Cloudy', 'Night']
    else:
        raise ValueError("Environment not available. Valid environments: FR_A, FR_B, SA_A, SA_B")
    return condIlum


def get_img_dir(imgFormat):
    if imgFormat == "RGB":
        directory = os.path.join(PARAMS.datasetDir, "COLD")
    elif imgFormat == "d":
        directory = os.path.join(PARAMS.datasetDir, "DEPTH_COLD")
    else:
        raise ValueError("Non-valid image format. Valid formats: RGB, d, RGBd")
    return directory


def process_image(image, tf):
    image = Image.open(image)
    if tf is not None:
        image = tf(image)
    return image


def build_visual_model(dataloader, model):
    descriptors, coords = [], []

    for i, vmData in enumerate(dataloader, 0):
        img, imgCoords = vmData
        img = img.to(device)
        output = model(img)
        descriptors.append(output)
        coords.append(imgCoords.detach().numpy()[0])
    descriptors = torch.squeeze(torch.stack(descriptors)).to(device)
    treeCoords = KDTree(coords, leaf_size=2)
    return descriptors, coords, treeCoords


def late_fusion(rgb, depth, method):
    if method == "concat":
        out = torch.cat((rgb, depth), dim=1)
    elif method == "sum":
        out = rgb + depth
    elif method == "weighted":
        w = PARAMS.w
        out = w * rgb + (1 - w) * depth
    else:
        raise ValueError("Non-valid method. Late fusion methods: concat, sum, weighted")
    return out



