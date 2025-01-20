"""
TEST CODE: PLACE RECOGNITION TASK

COMPARISON AMONG SEVERAL LATE FUSION METHODS: concat, sum and weighted sum
Other studied parameters: descriptor size (64, 128, 256, 512 and mixtures)

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
import create_datasets
import create_figures
from config import PARAMS
from functions import create_path, get_cond_ilum, build_visual_model, late_fusion


device = torch.device(PARAMS.device if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

csvDir = create_path(os.path.join(PARAMS.csvDir, "RESULTS"))
figuresDir = create_path(os.path.join(PARAMS.figuresDir, "LF"))

kMax = PARAMS.kMax
env = PARAMS.testEnv
condIlum = get_cond_ilum(env)


with open(csvDir + "/ResultsLF.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Desc Length", "Method", "Ilum", "Geom error", "Min error", "Recall@1", "Recall@1%"])

    vmDataset_RGB = create_datasets.VisualModel(env=env, imgFormat="RGB")
    vmDataloader_RGB = DataLoader(vmDataset_RGB, shuffle=False, num_workers=0, batch_size=1)

    vmDataset_d = create_datasets.VisualModel(env=env, imgFormat="d")
    vmDataloader_d = DataLoader(vmDataset_d, shuffle=False, num_workers=0, batch_size=1)

    print(f"TEST LATE FUSION\n\n")

    lenList = PARAMS.lenList

    bestLen, bestError = "", 100

    for descLength in lenList:

        print(f"TEST Desc length {descLength}\n")

        savedModelsDir = PARAMS.modelsDir
        netRGBDir = os.path.join(savedModelsDir, "RGB", str(descLength))
        netdDir = os.path.join(savedModelsDir, "d", str(descLength))

        testNetRGB = os.path.join(netRGBDir, os.listdir(netRGBDir)[0])
        testNetd = os.path.join(netdDir, os.listdir(netdDir)[0])

        netRGB, netDepth = torch.load(testNetRGB).to(device), torch.load(testNetd).to(device)
        netRGB.eval()
        netDepth.eval()

        with torch.no_grad():

            """VISUAL MODEL"""
            desc_RGB, coordsVM, treeCoordsVM = build_visual_model(vmDataloader_RGB, netRGB)
            desc_d, _, _ = build_visual_model(vmDataloader_d, netDepth)

            methodsList = PARAMS.lf_methods

            bestMethod, bestMethodError = "", 100

            for method in methodsList:

                print(f"Late fusion method: {method}")
                descVM = late_fusion(desc_RGB, desc_d, method)

                recall = np.zeros((len(condIlum), kMax))
                geomError, minErrorPossible = np.zeros(len(condIlum)), np.zeros(len(condIlum))
                mapMethodDir = create_path(os.path.join(figuresDir, method))

                for ilum in condIlum:
                    idxIlum = condIlum.index(ilum)

                    print(f"Test {ilum}")

                    testDataset = create_datasets.Test_LF(illumination=ilum, env=env)
                    testDataloader = DataLoader(testDataset, num_workers=0, batch_size=1, shuffle=False)

                    coordsMapTest = []

                    for i, data in enumerate(testDataloader, 0):
                        img_RGB, img_d, coordsImgTest = data
                        img_RGB, img_d = img_RGB.to(device), img_d.to(device)

                        out_RGB, out_d = netRGB(img_RGB), netDepth(img_d)
                        output = late_fusion(out_RGB, out_d, method)
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

                    mapDir = create_path(os.path.join(mapMethodDir, str(descLength)))
                    # create_figures.display_coord_map(mapDir, coordsVM, coordsMapTest, kMax, ilum, env)

                    print(f"Geometric error: {geomError[idxIlum]} m")
                    print(f"Minimum reachable error: {minErrorPossible[idxIlum]} m\n")

                    writer.writerow([descLength, method, ilum, geomError[idxIlum], minErrorPossible[idxIlum],
                                     recall[idxIlum][0], recall[idxIlum][round(len(descVM)/100)]])

                avgGeomError = np.average(geomError)
                avgRecall, avgMinError = np.average(recall, axis=0), np.average(minErrorPossible)

                writer.writerow([descLength, method, "Average", avgGeomError, avgMinError,
                                 avgRecall[0], avgRecall[round(len(descVM)/100)]])

                if avgGeomError < bestMethodError:
                    bestMethod, bestMethodError = method, avgGeomError
                    if avgGeomError < bestError:
                        bestLen, bestError = descLength, avgGeomError

            if bestMethod != "":
                print(f"Best LF Method (Size {descLength}): {bestMethod}, Geometric error: {bestMethodError} m")
    if bestLen != "":
        print(f"Best LF Size: {descLength}, Geometric error: {bestError} m")
