"""
In this script, the architecture of the CNNs and the rest of models is designed
"""


import torch
import torch.nn as nn
import torch.nn.functional as F

from torchvision.models import VGG16_Weights
vgg16 = torch.hub.load('pytorch/vision:v0.12.0', 'vgg16', weights=VGG16_Weights.DEFAULT)


class CosPlace_RGB(nn.Module):

    def __init__(self, out_dim=512):
        super(CosPlace_RGB, self).__init__()
        self.backbone = vgg16.features
        self.aggregation = nn.Sequential(
            L2Norm(),
            GeM(),
            Flatten(),
            nn.Linear(512, out_dim),
            L2Norm()
        )

    def forward(self, x):
        out = self.backbone(x)
        out = self.aggregation(out)

        return out


class CosPlace_RGBd(nn.Module):

    def __init__(self, out_dim=512):
        super(CosPlace_RGBd, self).__init__()
        self.backbone = vgg16.features
        new_conv1 = nn.Conv2d(in_channels=4, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.backbone[0] = new_conv1
        self.aggregation = nn.Sequential(
            L2Norm(),
            GeM(),
            Flatten(),
            nn.Linear(512, out_dim),
            L2Norm()
        )

    def forward(self, x):
        out = self.backbone(x)
        out = self.aggregation(out)

        return out


class CosPlace_d(nn.Module):

    def __init__(self, out_dim=512):
        super(CosPlace_d, self).__init__()
        self.backbone = vgg16.features
        new_conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.backbone[0] = new_conv1
        self.aggregation = nn.Sequential(
            L2Norm(),
            GeM(),
            Flatten(),
            nn.Linear(512, out_dim),
            L2Norm()
        )

    def forward(self, x):
        out = self.backbone(x)
        out = self.aggregation(out)

        return out


class CosPlace_MF(nn.Module):

    def __init__(self, out_dim=512):
        super(CosPlace_MF, self).__init__()
        self.aggregation = nn.Sequential(
            L2Norm(),
            GeM(),
            Flatten(),
            nn.Linear(1024, out_dim),
            L2Norm()
        )

    def forward(self, rgb, depth):
        out = torch.cat((rgb, depth), dim=1)
        out = self.aggregation(out)

        return out


class MonolayerPerceptron(nn.Module):
    def __init__(self, in_dim=1024, out_dim=2048):
        super(MonolayerPerceptron, self).__init__()
        self.fc = nn.Linear(in_dim, out_dim)

    def forward(self, x):
        x = self.fc(x)
        return x


class MLP_2layers(nn.Module):
    def __init__(self, in_dim=1024, mid_dim=4096, out_dim=1024):
        super(MLP_2layers, self).__init__()
        self.fc1 = nn.Linear(in_dim, mid_dim)
        self.fc2 = nn.Linear(mid_dim, out_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class L2Norm(nn.Module):
    def __init__(self, dim=1):
        super().__init__()
        self.dim = dim

    def forward(self, x):
        return F.normalize(x, p=2.0, dim=self.dim)


class Flatten(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        assert x.shape[2] == x.shape[3] == 1, f"{x.shape[2]} != {x.shape[3]} != 1"
        return x[:, :, 0, 0]


class GeM(nn.Module):
    def __init__(self, p=3, eps=1e-6):
        super(GeM, self).__init__()
        self.p = torch.nn.Parameter(torch.ones(1) * p)
        self.eps = eps

    def forward(self, x):
        return gem(x, p=self.p, eps=self.eps)


def gem(x, p=3, eps=1e-6):
    return F.avg_pool2d(x.clamp(min=eps).pow(p), (x.size(-2), x.size(-1))).pow(1. / p)
