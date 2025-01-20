"""
TEST CODE: PLACE RECOGNITION TASK

COMPARISON AMONG CNNs TRAINED WITH RGB IMAGES, DEPTH MAPS AND RGBd IMAGES (EARLY FUSION)
Other studied parameters: descriptor size (64, 128, 256, 512)

Test datasets:
Freiburg Part A (FR_A) and Part B (FR_B) and Saarbrücken Part A (SA_A) and Part B (SA_B)

Lighting conditions: Cloudy, Night and Sunny

Visual model dataset: the training set is employed as visual model

The test is performed in one step:
    -each test image is compared with the images of the visual model of the entire map
    -the nearest neighbour indicates the retrieved coordinates
"""

import csv
import os
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

import create_datasets
import create_figures
from config import PARAMS
from functions import create_path, get_cond_ilum, build_visual_model


device = torch.device(PARAMS.device if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

csvDir = create_path(os.path.join(PARAMS.csvDir, "RESULTS"))
figuresDir = create_path(os.path.join(PARAMS.figuresDir, "EF"))

kMax = PARAMS.kMax
env = PARAMS.testEnv
condIlum = get_cond_ilum(env)

with open(csvDir + "/ResultsEF.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ImgFormat", "Output Size", "Net", "Ilum", "Geom error", "Min error", "Recall@1", "Recall@1%"])

    bestFormat, bestError = "", 100

    baseModelDir = PARAMS.modelsDir
    formatList, lenList = PARAMS.formatList, PARAMS.lenList
    for imgFormat in formatList:

        if imgFormat in ["RGB", "d"]:
            vmDataset = create_datasets.VisualModel(env=env, imgFormat=imgFormat)
        elif imgFormat == "RGBd":
            vmDataset = create_datasets.VisualModel_EF(env=env)
        else:
            continue

        vmDataloader = DataLoader(vmDataset, shuffle=False, num_workers=0, batch_size=1)
        formatDir, mapFormatDir = os.path.join(baseModelDir, imgFormat), os.path.join(figuresDir, imgFormat)

        bestLen, bestFormatError = "", 100

        for descLength in lenList:
            print(f"TEST {imgFormat}, output size: {descLength}, Environment: {env}\n")
            bestNet, bestLenError = "", 100
            netDir = os.path.join(formatDir, str(descLength))

            testNets = os.listdir(netDir)
            for testNet in testNets:
                testDir = os.path.join(netDir, testNet)
                net = torch.load(testDir).to(device)
                net.eval()
                print(f"Net: {testNet}\n")

                with torch.no_grad():

                    descVM, coordsVM, treeCoordsVM = build_visual_model(vmDataloader, net)

                    recall = np.zeros((len(condIlum), kMax))
                    geomError, minErrorPossible = np.zeros(len(condIlum)), np.zeros(len(condIlum))

                    for ilum in condIlum:
                        idxIlum = condIlum.index(ilum)

                        print(f"Test {ilum}")

                        if imgFormat in ["RGB", "d"]:
                            testDataset = create_datasets.Test(illumination=ilum, env=env, imgFormat=imgFormat)
                        elif imgFormat == "RGBd":
                            testDataset = create_datasets.Test_EF(illumination=ilum, env=env)
                        else:
                            raise ValueError("Non-valid image format. Valid formats: RGB, d, RGBd")
                        testDataloader = DataLoader(testDataset, num_workers=0, batch_size=1, shuffle=False)

                        coordsMapTest = []

                        for i, data in enumerate(testDataloader, 0):
                            imgTest, coordsImgTest = data
                            imgTest = imgTest.to(device)

                            output = net(imgTest)
                            coordsImgTest = coordsImgTest.detach().numpy()[0]

                            distances = F.pairwise_distance(output, descVM).reshape(1, -1)
                            idxMinPred = torch.argmin(distances).cpu().detach().numpy()

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

                        mapDir = create_path(os.path.join(mapFormatDir, str(descLength)))
                        create_figures.display_coord_map(mapDir, coordsVM, coordsMapTest, kMax, ilum, env)

                        print(f"Geometric error: {geomError[idxIlum]} m")
                        print(f"Minimum reachable error: {minErrorPossible[idxIlum]} m\n")

                        writer.writerow([imgFormat, descLength, testNet, ilum,
                                         geomError[idxIlum], minErrorPossible[idxIlum],
                                         recall[idxIlum][0], recall[idxIlum][round(len(vmDataloader)/100)]])

                    avgGeomError, avgMinError = np.average(geomError), np.average(minErrorPossible)
                    avgRecall = np.average(recall, axis=0)

                    writer.writerow([imgFormat, descLength, testNet, "Average", avgGeomError, avgMinError,
                                     avgRecall[0], avgRecall[round(len(vmDataloader)/100)]])

                    if avgGeomError < bestLenError:
                        bestNet, bestLenError = testNet, avgGeomError
                        if avgGeomError < bestFormatError:
                            bestLen, bestFormatError = descLength, avgGeomError
                            if avgGeomError < bestError:
                                bestFormat, bestError = imgFormat, avgGeomError

            if bestNet != "":
                print(f"Best Net {imgFormat}, size {descLength}: {bestNet}, Geometric error: {bestLenError} m")
        if bestNet != "":
            print(f"Best Size {imgFormat}: {bestLen}, Geometric error: {bestFormatError} m")
    if bestNet != "":
        print(f"Best Format: {bestFormat}, Geometric error: {bestError} m")
