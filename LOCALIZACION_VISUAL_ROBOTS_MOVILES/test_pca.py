"""
TEST CODE: PLACE RECOGNITION TASK

LATE FUSION METHODS: Principal Component Analysis (PCA)
Other studied parameters: descriptor size (64, 128, 256, 512), number of components (64, 128, 256),
                          concatenation or weighted sum of input descriptors

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
from sklearn.neighbors import KDTree
import torch.nn.functional as F
import create_figures
import create_datasets
from sklearn.decomposition import PCA
from functions import create_path, get_cond_ilum, build_visual_model, late_fusion
from config import PARAMS


device = torch.device(PARAMS.device if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

csvDir = create_path(os.path.join(PARAMS.csvDir, "RESULTS"))
figuresDir = create_path(os.path.join(PARAMS.figuresDir, "LF"))

kMax = PARAMS.kMax

env = PARAMS.testEnv
condIlum = get_cond_ilum(env)


with open(csvDir + "/PCAResults.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Num Components", "Desc Length", "Ilum", "Geom error", "Min error", "Recall@1", "Recall@1%"])

    vmRGBDataset = create_datasets.VisualModel(env=env, imgFormat="RGB")
    vmRGBDataloader = DataLoader(vmRGBDataset, shuffle=False, num_workers=0, batch_size=1)

    vmDepthDataset = create_datasets.VisualModel(env=env, imgFormat="d")
    vmDepthDataloader = DataLoader(vmDepthDataset, shuffle=False, num_workers=0, batch_size=1)

    # convertir en lista
    PCAvalues = PARAMS.numComponents_PCA
    for n in PCAvalues:

        print(f"TEST PCA: Num. components = {n}\n\n")

        lenList = PARAMS.lenList
        w = PARAMS.w
        pca = PCA(n_components=n)
        nDir = create_path(os.path.join(figuresDir, str(n)))

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
                desc_RGB, coordsVM, treeCoordsVM = build_visual_model(vmRGBDataloader, netRGB)
                desc_d, _, _ = build_visual_model(vmDepthDataloader, netDepth)

                if PARAMS.PCA_weighted:
                    descVM = late_fusion(desc_RGB, desc_d, "weighted").cpu().detach().numpy()
                else:
                    descVM = late_fusion(desc_RGB, desc_d, "concat").cpu().detach().numpy()

                pca.fit(descVM)
                descPCA = pca.transform(descVM)
                treeDescVM = KDTree(descPCA, leaf_size=2)

                """TEST"""

                recall = np.zeros((len(condIlum), kMax))
                geomError, minErrorPossible = np.zeros(len(condIlum)), np.zeros(len(condIlum))

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
                        if PARAMS.PCA_weighted:
                            output = late_fusion(out_RGB, out_d, "weighted").cpu().detach().numpy()
                        else:
                            output = late_fusion(out_RGB, out_d, "concat").cpu().detach().numpy()
                        descTestPCA = pca.transform(output.reshape(1, -1))
                        coordsImgTest = coordsImgTest.detach().numpy()[0]

                        _, indexes = treeDescVM.query(descTestPCA.reshape(1, -1), k=1)
                        idxMinPred = indexes[0][0]

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

                    mapDir = create_path(os.path.join(figuresDir, str(n), str(descLength)))
                    # create_figures.display_coord_map(figuresDir, coordsVM, coordsMapTest, kMax, ilum, env)

                    print(f"Geometric error: {geomError[idxIlum]} m")
                    print(f"Minimum reachable error: {minErrorPossible[idxIlum]} m\n")

                    writer.writerow([n, descLength, ilum, geomError[idxIlum], minErrorPossible[idxIlum],
                                     recall[idxIlum][0], recall[idxIlum][round(len(descVM)/100)]])

                avgRecall = np.average(recall, axis=0)
                avgGeomError, avgMinError = np.average(geomError), np.average(minErrorPossible)

                writer.writerow([n, descLength, "Average", avgGeomError, avgMinError,
                                 avgRecall[0], avgRecall[round(len(descVM)/100)]])
