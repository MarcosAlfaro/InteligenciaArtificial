"""
TEST CODE: PLACE RECOGNITION TASK

LATE FUSION METHODS: Monolayer and Multilayer Perceptrons
Other studied parameters: descriptor size (64, 128, 256, 512), architecture of the MLP

In this case, a small training is required (Training length: 2000 triplet samples, same conditions as training of CNNs)

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
import torch.nn.functional as F
from torch.utils.data import DataLoader
import losses
import create_datasets
import create_figures
from models import MonolayerPerceptron, MLP_2layers
from config import PARAMS
from functions import create_path, get_cond_ilum, build_visual_model

device = torch.device(PARAMS.device if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

csvDir = create_path(os.path.join(PARAMS.csvDir, "RESULTS"))
figuresDir = create_path(os.path.join(PARAMS.figuresDir, "LF"))

env = PARAMS.testEnv
condIlum = get_cond_ilum(env)
kMax = PARAMS.kMax

trainDataset = create_datasets.Train_MLP()
trainDataloader = DataLoader(trainDataset, shuffle=False, num_workers=0, batch_size=PARAMS.batchSize)

vmDataset_RGB = create_datasets.VisualModel(env=env, imgFormat="RGB")
vmDataloader_RGB = DataLoader(vmDataset_RGB, shuffle=False, num_workers=0, batch_size=1)

vmDataset_d = create_datasets.VisualModel(env=env, imgFormat="d")
vmDataloader_d = DataLoader(vmDataset_d, shuffle=False, num_workers=0, batch_size=1)

"""NETWORK TRAINING"""

with open(csvDir + "/MLPTrainData.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Architecture", "Ilum", "Geom error", "Min error", "Recall@1", "Recall@1%"])

    lossFunction = "batch hard"
    margin = PARAMS.margin

    criterion = losses.BatchHardLoss()

    savedModelsDir = PARAMS.modelsDir
    sizeRGB, sizeDepth = PARAMS.sizeRGB_MLP, PARAMS.sizeDepth_MLP
    netRGBDir = os.path.join(savedModelsDir, "RGB", str(sizeRGB))
    netRGBDir = os.path.join(netRGBDir, os.listdir(netRGBDir)[0])
    netDepthDir = os.path.join(savedModelsDir, "d", str(sizeDepth))
    netDepthDir = os.path.join(netDepthDir, os.listdir(netDepthDir)[0])

    architecture = PARAMS.MLP_architecture
    if len(architecture) == 2:
        net = MonolayerPerceptron(in_dim=sizeRGB + sizeDepth, out_dim=architecture[1]).to(device)
        architecture_str = str(architecture[0]) + str(architecture[1])

    elif len(architecture) == 3:
        net = MLP_2layers(in_dim=sizeRGB + sizeDepth, out_dim=architecture[2], mid_dim=architecture[1]).to(device)
        architecture_str = str(architecture[0]) + str(architecture[1]) + str(architecture[2])

    else:
        raise ValueError("MLP must have 2 or 3 layers")
    netDir = create_path(os.path.join(savedModelsDir, "MLP", architecture_str))

    optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    print(f"\nTRAIN MLP, architecture: {architecture_str}")

    bestError = 1000

    for i, data in enumerate(trainDataloader, 0):

        anc_RGB, pos_RGB, neg_RGB, anc_d, pos_d, neg_d = data
        anc_RGB, pos_RGB, neg_RGB = anc_RGB.to(device), pos_RGB.to(device), neg_RGB.to(device)
        anc_d, pos_d, neg_d = anc_d.to(device), pos_d.to(device), neg_d.to(device)

        optimizer.zero_grad()

        netRGB, netDepth = torch.load(netRGBDir).to(device), torch.load(netDepthDir).to(device)
        netRGB.eval()
        netDepth.eval()
        with torch.no_grad():
            outRGB1, outRGB2, outRGB3 = netRGB(anc_RGB), netRGB(pos_RGB), netRGB(neg_RGB)
            outDepth1, outDepth2, outDepth3 = netDepth(anc_d), netDepth(pos_d), netDepth(neg_d)

        input1, input2, input3 = torch.cat((outRGB1, outDepth1), dim=1), torch.cat((outRGB2, outDepth2), dim=1), \
                                 torch.cat((outRGB3, outDepth3), dim=1)

        output1, output2, output3 = net(input1), net(input2), net(input3)

        loss = criterion(output1, output2, output3, margin)
        loss.backward()

        optimizer.step()

        if i == int(PARAMS.stopTrainingMLP / PARAMS.batchSize):
            break

    netName = os.path.join(netDir, "net_" + architecture_str)
    torch.save(net, netName)

    net.eval()
    with torch.no_grad():

        """VISUAL MODEL"""
        desc_RGB, coordsVM, treeCoordsVM = build_visual_model(vmDataloader_RGB, netRGB)
        desc_d, _, _ = build_visual_model(vmDataloader_d, netDepth)

        descVM = []
        descRGBd = torch.cat((desc_RGB, desc_d), dim=1)
        for i in range(len(vmDataloader_RGB)):
            output = net(descRGBd[i, :])
            descVM.append(output)
        descVM = torch.squeeze(torch.stack(descVM)).to(device)

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
                descRGBd = torch.cat((out_RGB, out_d), dim=1)
                output = net(descRGBd)
                coordsImgTest = coordsImgTest.detach().numpy()[0]

                distances = F.pairwise_distance(output, descVM).reshape(1, -1)
                idxMinPred = torch.argmin(distances)

                geomDistances, idxGeom = treeCoordsVM.query(coordsImgTest.reshape(1, -1), k=kMax)
                idxMinReal = idxGeom[0][0]

                coordsPredictedImg, coordsClosestImg = coordsVM[idxMinPred], coordsVM[idxMinReal]

                if idxMinPred in idxGeom[0]:
                    label = str(idxGeom[0].tolist().index(idxMinPred) + 1)
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

            mapDir = create_path(os.path.join(figuresDir, architecture_str))
            create_figures.display_coord_map(mapDir, coordsVM, coordsMapTest, kMax, ilum, env)

            print(f"Geometric error: {geomError[idxIlum]} m")
            print(f"Minimum reachable error: {minErrorPossible[idxIlum]} m\n")

            writer.writerow([architecture_str, ilum, geomError[idxIlum], minErrorPossible[idxIlum],
                             recall[idxIlum][0], recall[idxIlum][round(len(descVM) / 100)]])

        avgGeomError, avgMinError = np.average(geomError), np.average(minErrorPossible)
        avgRecall = np.average(recall, axis=0)

        writer.writerow([architecture_str, "Average", avgGeomError, avgMinError,
                         avgRecall[0], avgRecall[round(len(descVM) / 100)]])
