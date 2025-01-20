"""
THIS PROGRAM CONTAINS THE TRIPLET LOSS FUNCTION TO TRAIN THE NETWORK MODELS
Training scripts will call this class to use the loss
"""


import torch
import torch.nn.functional as F
import torch.nn as nn


class BatchHardLoss(nn.Module):
    def __init__(self, margin=0.5):
        super(BatchHardLoss, self).__init__()
        self.margin = margin

    def forward(self, anchor, positive, negative, margin):
        distance_positive = F.pairwise_distance(anchor, positive, keepdim=True)
        distance_negative = F.pairwise_distance(anchor, negative, keepdim=True)
        hardest_positive = torch.max(distance_positive)
        hardest_negative = torch.min(distance_negative)
        loss = torch.relu(hardest_positive - hardest_negative + margin)

        return loss
