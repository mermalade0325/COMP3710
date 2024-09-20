import torch
import torch.nn as nn

class CeDiceLoss(nn.Module):
    def __init__(self, num_classes):
        super(CeDiceLoss, self).__init__()
        self.num_classes = num_classes
        self.ce_loss = nn.CrossEntropyLoss()
    
    def forward(self, predictions, targets):
        # Compute Cross Entropy Loss
        ce = self.ce_loss(predictions, targets)
        
        # Compute Dice Loss
        smooth = 1e-6  # To prevent division by zero
        preds = torch.softmax(predictions, dim=1)
        preds_flat = preds.view(-1)
        targets_flat = targets.view(-1)

        intersection = (preds_flat * targets_flat).sum()
        dice_loss = 1 - (2. * intersection + smooth) / (preds_flat.sum() + targets_flat.sum() + smooth)
        
        return ce + dice_loss

# You can add more loss functions as needed below