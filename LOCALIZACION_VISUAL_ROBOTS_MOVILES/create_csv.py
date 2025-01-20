"""
This script is used to create the CSV needed for the training, validation, visual model and test.
It must be executed before any other script.
"""


import os
import csv
import random
import numpy as np
from sklearn.neighbors import KDTree
from functions import get_coords, get_env, get_cond_ilum
from config import PARAMS


csvDir = PARAMS.csvDir


def train(trainLength, tree, rPos, rNeg):

    with open(csvDir + '/Train.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ImgAnc", "ImgPos", "ImgNeg"])

        for i in range(trainLength):
            idxAnc = random.randrange(len(imgsList))
            imgAnc = imgsList[idxAnc]
            coordsAnc = coordsList[idxAnc]

            indexes = tree.query_radius(coordsAnc.reshape(1, -1), r=rPos)[0]
            idxPos = random.choice(indexes)
            while idxAnc == idxPos:
                idxPos = random.choice(indexes)
            imgPos = imgsList[idxPos]

            indexes = tree.query_radius(coordsAnc.reshape(1, -1), r=rNeg)[0]
            idxNeg = random.randrange(len(imgsList))
            while idxNeg in indexes or idxAnc == idxNeg:
                idxNeg = random.randrange(len(imgsList))
            imgNeg = imgsList[idxNeg]

            writer.writerow([imgAnc, imgPos, imgNeg])
    return


def validation():
    valDatasetDir = os.path.join(PARAMS.datasetDir, "COLD", "FRIBURGO_A")
    valDir = os.path.join(valDatasetDir, "Validation")

    with open(csvDir + '/Validation.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Img", "CoordX", "CoordY"])

        rooms = os.listdir(valDir)
        for room in rooms:
            roomDir = os.path.join(valDir, room)
            imgsVal = os.listdir(roomDir)
            for image in imgsVal:
                x, y = get_coords(image)
                writer.writerow([os.path.join(room, image), x, y])
    return


def test(il, env):

    testDatasetDir = os.path.join(PARAMS.datasetDir, "COLD", get_env(env))
    testDir = os.path.join(testDatasetDir, "Test" + il)
    if not os.path.exists(testDir):
        return
    with open(csvDir + '/Test' + il + env + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Img", "CoordX", "CoordY"])
        rooms = os.listdir(testDir)
        for room in rooms:
            roomDir = os.path.join(testDir, room)
            imgsTest = os.listdir(roomDir)
            for image in imgsTest:
                x, y = get_coords(image)
                writer.writerow([os.path.join(room, image), x, y])
    return


def visual_model(env):
    vmDatasetDir = os.path.join(PARAMS.datasetDir, "COLD", get_env(env))
    vmDir = os.path.join(vmDatasetDir, "Train")

    with open(csvDir + '/VisualModel' + env + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Img", "CoordX", "CoordY"])

        imgsVM, coordsVM = [], []
        rooms = os.listdir(vmDir)
        for room in rooms:
            roomDir = os.path.join(vmDir, room)
            imgsDir = os.listdir(roomDir)
            for image in imgsDir:
                x, y = get_coords(image)
                imgsVM.append(os.path.join(room, image))
                coordsVM.append(np.array([x, y]))
                writer.writerow([os.path.join(room, image), x, y])

    return imgsVM, coordsVM


envs = PARAMS.envs
for env in envs:
    imgsList, coordsList = visual_model(env=env)
    condIlum = get_cond_ilum(env)
    for ilum in condIlum:
        test(il=ilum, env=env)
treeVM = KDTree(coordsList, leaf_size=2)


train(trainLength=PARAMS.trainLength, tree=treeVM, rPos=PARAMS.rPos, rNeg=PARAMS.rNeg)
validation()

