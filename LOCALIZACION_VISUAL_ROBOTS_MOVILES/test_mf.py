"""
TEST CODE: PLACE RECOGNITION TASK (MIDDLE FUSION)
Other studied parameters: descriptor size (64, 128, 256, 512)

Test datasets:
Freiburg Part A (FR_A) and Part B (FR_B) and Saarbrücken Part A (SA_A) and Part B (SA_B)

Lighting conditions: Cloudy, Night and Sunny

Visual model dataset: the training set is employed as visual model

The test is performed in one step:
    -each test image is compared with the images of the visual model of the entire map
    -the nearest neighbour indicates the retrieved coordinates
"""

import torch
import os
import csv
import numpy as np
from torch.utils.data import DataLoader
import torch.nn.functional as F
from sklearn.neighbors import KDTree
import create_datasets
import create_figures
import models
from functions import create_path, get_cond_ilum
from config import PARAMS


device = torch.device(PARAMS.device if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

csvDir = create_path(os.path.join(PARAMS.csvDir, "RESULTS"))
figuresDir = create_path(os.path.join(PARAMS.figuresDir, "MF"))

kMax = PARAMS.kMax

env = PARAMS.testEnv
condIlum = get_cond_ilum(env)

with open(csvDir + "/ResultsMF.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Output Size", "Ilum", "Geom error", "Min error", "Recall@1", "Recall@1%"])

    savedModelsDir = PARAMS.modelsDir
    netRGBDir = os.path.join(savedModelsDir, "RGB", "512")
    netRGB = torch.load(os.path.join(netRGBDir, os.listdir(netRGBDir)[0]))
    netRGB = netRGB.backbone.to(device)
    netRGB.eval()

    netDepthDir = os.path.join(savedModelsDir, "d", "512")
    netDepth = torch.load(os.path.join(netDepthDir, os.listdir(netDepthDir)[0])).to(device)
    netDepth = netDepth.backbone.to(device)
    netDepth.eval()

    vmDataset = create_datasets.VisualModel_MF(env=env)
    vmDataloader = DataLoader(vmDataset, shuffle=False, num_workers=0, batch_size=1)

    bestLen, bestError = "", 100

    lenList = PARAMS.lenList
    for descLength in lenList:

        print(f"TEST MIDDLE FUSION, output size: {descLength}\n")

        net = models.CosPlace_MF(out_dim=int(descLength)).to(device)
        RGB_weights = torch.load(PARAMS.baseModel_MF)
        with torch.no_grad():
            net.aggregation[1].p.copy_(RGB_weights.aggregation[1].p)
        net.eval()

        with torch.no_grad():

            """VISUAL MODEL"""

            descVM, coordsVM = [], []
            for i, vmData in enumerate(vmDataloader, 0):
                img_RGB, img_d, coords = vmData
                img_RGB, img_d = img_RGB.to(device), img_d.to(device)
                out_RGB, out_d = netRGB(img_RGB), netDepth(img_d)
                output = net(out_RGB, out_d)
                descVM.append(output)
                coordsVM.append(coords.detach().numpy()[0])
            descVM = torch.squeeze(torch.stack(descVM)).to(device)
            treeCoordsVM = KDTree(coordsVM, leaf_size=2)

            """
            
            
            
            
            
            """

            recall = np.zeros((len(condIlum), kMax))
            geomError, minErrorPossible = np.zeros(len(condIlum)), np.zeros(len(condIlum))

            for ilum in condIlum:
                idxIlum = condIlum.index(ilum)

                print(f"Test {ilum}")

                testDataset = create_datasets.Test_MF(illumination=ilum, env=env)
                testDataloader = DataLoader(testDataset, num_workers=0, batch_size=1, shuffle=False)

                coordsMapTest = []

                for i, data in enumerate(testDataloader, 0):
                    img_RGB, img_d, coordsImgTest = data
                    img_RGB, img_d = img_RGB.to(device), img_d.to(device)
                    out_RGB, out_d = netRGB(img_RGB), netDepth(img_d)
                    output = net(out_RGB, out_d)
                    coordsImgTest = coordsImgTest.detach().numpy()[0]

                    distances = F.pairwise_distance(output, descVM).reshape(1, -1)
                    idxMinPred = torch.argmin(distances)

                    geomDistances, idxGeom = treeCoordsVM.query(coordsImgTest.reshape(1, -1), k=kMax)
                    idxMinReal = idxGeom[0][0]

                    coordsPredictedImg, coordsClosestImg = coordsVM[idxMinPred], coordsVM[idxMinReal]

                    if idxMinPred in idxGeom[0]:
                        label = str(idxGeom[0].tolist().index(idxMinPred)+1)
                        recall[idxIlum][idxGeom[0].tolist().index(idxMinPred):] += 1
                    else:
                        label = "F"

                    coordsMapTest.append([coordsPredictedImg[0], coordsPredictedImg[1],
                                          coordsImgTest[0], coordsImgTest[1], label])

                    geomError[idxIlum] += np.linalg.norm(coordsImgTest - coordsPredictedImg)
                    minErrorPossible[idxIlum] += np.linalg.norm(coordsImgTest - coordsClosestImg)

                recall[idxIlum] *= 100 / len(testDataloader)
                geomError[idxIlum] /= len(testDataloader)
                minErrorPossible[idxIlum] /= len(testDataloader)

                mapDir = create_path(os.path.join(figuresDir, str(descLength)))
                # create_figures.display_coord_map(mapDir, coordsVM, coordsMapTest, kMax, ilum, env)

                print(f"Geometric error: {geomError[idxIlum]} m")
                print(f"Minimum reachable error: {minErrorPossible[idxIlum]} m\n")

                writer.writerow([descLength, ilum, geomError[idxIlum], minErrorPossible[idxIlum],
                                 recall[idxIlum][0], recall[idxIlum][round(len(descVM)/100)]])

            avgGeomError, avgMinError = np.average(geomError), np.average(minErrorPossible)
            avgRecall = np.average(recall, axis=0)

            writer.writerow([descLength, "Average", avgGeomError, avgMinError,
                             avgRecall[0], avgRecall[round(len(descVM)/100)]])

            if avgGeomError < bestError:
                bestLen, bestError = descLength, avgGeomError

    if bestLen != "":
        print(f"Best Size: {bestLen}, Geometric error: {bestError} m")
