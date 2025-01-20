"""
THIS PROGRAM CONTAINS ALL THE CLASSES THAT CREATE THE DATALOADES OF THE TRAINING, VALIDATION, VISUAL MODEL AND TEST
These classes will be called by training and test scripts
"""


import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import pandas as pd
import numpy as np
import os
from config import PARAMS
from functions import get_env, get_img_dir, process_image


csvDir = PARAMS.csvDir


RGBDir = os.path.join(PARAMS.datasetDir, "COLD")
depthDir = os.path.join(PARAMS.datasetDir, "DEPTH_COLD")


class Train(Dataset):

    def __init__(self, imgFormat="RGB", transform=transforms.ToTensor()):

        trainCSV = pd.read_csv(csvDir + '/Train.csv')
        self.imgDir = get_img_dir(imgFormat)

        self.imgsAnc, self.imgsPos, self.imgsNeg = trainCSV['ImgAnc'], trainCSV['ImgPos'], trainCSV['ImgNeg']
        self.transform = transform

    def __getitem__(self, index):

        imgAnc, imgPos, imgNeg = self.imgsAnc[index], self.imgsPos[index], self.imgsNeg[index]

        imgAnc = os.path.join(self.imgDir, "FRIBURGO_A", "Train", imgAnc)
        imgPos = os.path.join(self.imgDir, "FRIBURGO_A", "Train", imgPos)
        imgNeg = os.path.join(self.imgDir, "FRIBURGO_A", "Train", imgNeg)

        anchor = process_image(imgAnc, self.transform)
        positive = process_image(imgPos, self.transform)
        negative = process_image(imgNeg, self.transform)

        return anchor, positive, negative

    def __len__(self):
        return len(self.imgsAnc)


class Validation(Dataset):

    def __init__(self, imgFormat="RGB", transform=transforms.ToTensor()):

        valCSV = pd.read_csv(csvDir + '/Validation.csv')
        self.imgDir = get_img_dir(imgFormat)

        self.imgList, self.coordX, self.coordY = valCSV['Img'], valCSV['CoordX'], valCSV["CoordY"]
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img = os.path.join(self.imgDir, "FRIBURGO_A", "Validation", img)
        img = process_image(img, self.transform)

        return img, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class Test(Dataset):

    def __init__(self, illumination, env="FR_A", imgFormat="RGB", transform=transforms.ToTensor()):

        testCSV = pd.read_csv(csvDir + '/Test' + illumination + env + '.csv')
        self.env, self.ilum, self.imgDir = get_env(env), illumination, get_img_dir(imgFormat)

        self.imgList, self.coordX, self.coordY = testCSV['Img'], testCSV['CoordX'], testCSV['CoordY']
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img = os.path.join(self.imgDir, self.env, "Test" + self.ilum, img)
        img = process_image(img, self.transform)

        return img, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class VisualModel(Dataset):

    def __init__(self, env="FR_A", imgFormat="RGB", transform=transforms.ToTensor()):

        vmCSV = pd.read_csv(csvDir + '/VisualModel' + env + '.csv')
        self.env, self.imgDir = get_env(env), get_img_dir(imgFormat)

        self.imgList, self.coordX, self.coordY = vmCSV['Img'], vmCSV['CoordX'], vmCSV['CoordY']
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img = os.path.join(self.imgDir, self.env, "Train", img)
        img = process_image(img, self.transform)

        return img, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class Train_EF(Dataset):

    def __init__(self, transform=transforms.ToTensor()):

        trainCSV = pd.read_csv(csvDir + '/Train.csv')

        self.imgsAnc, self.imgsPos, self.imgsNeg = trainCSV['ImgAnc'], trainCSV['ImgPos'], trainCSV['ImgNeg']
        self.transform = transform

    def __getitem__(self, index):

        imgAnc, imgPos, imgNeg = self.imgsAnc[index], self.imgsPos[index], self.imgsNeg[index]

        imgAnc_RGB = os.path.join(RGBDir, "FRIBURGO_A", "Train", imgAnc)
        imgPos_RGB = os.path.join(RGBDir, "FRIBURGO_A", "Train", imgPos)
        imgNeg_RGB = os.path.join(RGBDir, "FRIBURGO_A", "Train", imgNeg)

        anc_RGB = process_image(imgAnc_RGB, self.transform)
        pos_RGB = process_image(imgPos_RGB, self.transform)
        neg_RGB = process_image(imgNeg_RGB, self.transform)

        imgAnc_d = os.path.join(depthDir, "FRIBURGO_A", "Train", imgAnc)
        imgPos_d = os.path.join(depthDir, "FRIBURGO_A", "Train", imgPos)
        imgNeg_d = os.path.join(depthDir, "FRIBURGO_A", "Train", imgNeg)

        anc_d = process_image(imgAnc_d, self.transform)
        pos_d = process_image(imgPos_d, self.transform)
        neg_d = process_image(imgNeg_d, self.transform)

        anchor, positive, negative = (torch.cat((anc_RGB, anc_d), dim=0),
                                      torch.cat((pos_RGB, pos_d), dim=0),
                                      torch.cat((neg_RGB, neg_d), dim=0))

        return anchor, positive, negative

    def __len__(self):
        return len(self.imgsAnc)


class Validation_EF(Dataset):

    def __init__(self, transform=transforms.ToTensor()):

        valCSV = pd.read_csv(csvDir + '/Validation.csv')

        self.imgList, self.coordX, self.coordY = valCSV['Img'], valCSV['CoordX'], valCSV["CoordY"]
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img_RGB = os.path.join(RGBDir, "FRIBURGO_A", "Validation", img)
        img_RGB = process_image(img_RGB, self.transform)

        img_d = os.path.join(depthDir, "FRIBURGO_A", "Validation", img)
        img_d = process_image(img_d, self.transform)

        img = torch.cat((img_RGB, img_d), dim=0)

        return img, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class Test_EF(Dataset):

    def __init__(self, illumination, env="FR_A", transform=transforms.ToTensor()):

        testCSV = pd.read_csv(csvDir + '/Test' + illumination + env + '.csv')
        self.ilum, self.env = illumination, get_env(env)

        self.imgList, self.coordX, self.coordY = testCSV['Img'], testCSV['CoordX'], testCSV['CoordY']
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img_RGB = os.path.join(RGBDir, self.env, "Test" + self.ilum, img)
        img_RGB = process_image(img_RGB, self.transform)

        img_d = os.path.join(depthDir, self.env, "Test" + self.ilum, img)
        img_d = process_image(img_d, self.transform)

        img = torch.cat((img_RGB, img_d), dim=0)

        return img, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class VisualModel_EF(Dataset):

    def __init__(self, env="FR_A", transform=transforms.ToTensor()):

        vmCSV = pd.read_csv(csvDir + '/VisualModel' + env + '.csv')
        self.env = get_env(env)

        self.imgList, self.coordX, self.coordY = vmCSV['Img'], vmCSV['CoordX'], vmCSV['CoordY']
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img_RGB = os.path.join(RGBDir, self.env, "Train", img)
        img_RGB = process_image(img_RGB, self.transform)

        img_d = os.path.join(depthDir, self.env, "Train", img)
        img_d = process_image(img_d, self.transform)

        img = torch.cat((img_RGB, img_d), dim=0)

        return img, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class Test_LF(Dataset):

    def __init__(self, illumination, env="FR_A", transform=transforms.ToTensor()):

        testCSV = pd.read_csv(csvDir + '/Test' + illumination + env + '.csv')
        self.ilum, self.env = illumination, get_env(env)

        self.imgList, self.coordX, self.coordY = testCSV['Img'], testCSV['CoordX'], testCSV['CoordY']
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img_RGB = os.path.join(RGBDir, self.env, "Test" + self.ilum, img)
        img_RGB = process_image(img_RGB, self.transform)

        img_d = os.path.join(depthDir, self.env, "Test" + self.ilum, img)
        img_d = process_image(img_d, self.transform)

        return img_RGB, img_d, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class Test_MF(Dataset):

    def __init__(self, illumination, env="FR_A", transform=transforms.ToTensor()):

        testCSV = pd.read_csv(csvDir + '/Test' + illumination + env + '.csv')
        self.ilum, self.env = illumination, get_env(env)

        self.imgList, self.coordX, self.coordY = testCSV['Img'], testCSV['CoordX'], testCSV['CoordY']
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img_RGB = os.path.join(RGBDir, self.env, "Test" + self.ilum, img)
        img_RGB = process_image(img_RGB, self.transform)

        img_d = os.path.join(depthDir, self.env, "Test" + self.ilum, img)
        img_d = process_image(img_d, self.transform)

        return img_RGB, img_d, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class VisualModel_MF(Dataset):

    def __init__(self, env="FR_A", transform=transforms.ToTensor()):

        vmCSV = pd.read_csv(csvDir + '/VisualModel' + env + '.csv')
        self.env = get_env(env)

        self.imgList, self.coordX, self.coordY = vmCSV['Img'], vmCSV['CoordX'], vmCSV['CoordY']
        self.transform = transform

    def __getitem__(self, index):

        img, coordX, coordY = self.imgList[index], self.coordX[index], self.coordY[index]

        img_RGB = os.path.join(RGBDir, self.env, "Train", img)
        img_RGB = process_image(img_RGB, self.transform)

        img_d = os.path.join(depthDir, self.env, "Train", img)
        img_d = process_image(img_d, self.transform)

        return img_RGB, img_d, np.array([coordX, coordY])

    def __len__(self):
        return len(self.imgList)


class Train_MLP(Dataset):

    def __init__(self, transform=transforms.ToTensor()):

        trainCSV = pd.read_csv(csvDir + '/Train.csv')

        self.imgsAnc, self.imgsPos, self.imgsNeg = trainCSV['ImgAnc'], trainCSV['ImgPos'], trainCSV['ImgNeg']
        self.transform = transform

    def __getitem__(self, index):

        imgAnc, imgPos, imgNeg = self.imgsAnc[index], self.imgsPos[index], self.imgsNeg[index]

        imgAnc_RGB = os.path.join(RGBDir, "FRIBURGO_A", "Train", imgAnc)
        imgPos_RGB = os.path.join(RGBDir, "FRIBURGO_A", "Train", imgPos)
        imgNeg_RGB = os.path.join(RGBDir, "FRIBURGO_A", "Train", imgNeg)

        anc_RGB = process_image(imgAnc_RGB, self.transform)
        pos_RGB = process_image(imgPos_RGB, self.transform)
        neg_RGB = process_image(imgNeg_RGB, self.transform)

        imgAnc_d = os.path.join(depthDir, "FRIBURGO_A", "Train", imgAnc)
        imgPos_d = os.path.join(depthDir, "FRIBURGO_A", "Train", imgPos)
        imgNeg_d = os.path.join(depthDir, "FRIBURGO_A", "Train", imgNeg)

        anc_d = process_image(imgAnc_d, self.transform)
        pos_d = process_image(imgPos_d, self.transform)
        neg_d = process_image(imgNeg_d, self.transform)

        return anc_RGB, pos_RGB, neg_RGB, anc_d, pos_d, neg_d

    def __len__(self):
        return len(self.imgsAnc)
