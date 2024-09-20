# -*- coding: utf-8 -*-
"""
Train the Unet models here.
"""

import logging
import wandb
from models import UNet
from utils.losses import *
import torch
from torch.utils.data import DataLoader, random_split
from torch import optim
from tqdm import tqdm
import torch.nn.functional as F


# load dataset
in_channel = 1
label_num = 7

train_file_path = TRAIN_IMAGE_PATH
cp_path = MODEL_SAVE_PATH
train_dataset = UnetNiiDataset(train_file_path)

def train_model(
        model,
        device,
        epochs: int = 5,
        batch_size: int = 10,
        learning_rate: float = 1e-5,
        val_percent: float = 0.1,
        save_checkpoint: bool = True,
):
    # train/val split
    n_val = int(len(train_dataset) * val_percent)
    n_train = len(train_dataset) - n_val
    train_set, val_set = random_split(train_dataset, [n_train, n_val], 
                                    generator=torch.Generator().manual_seed(0))

    # Create data loaders
    train_loader = DataLoader(train_set, shuffle=True, batch_size=batch_size)
    val_loader = DataLoader(val_set, shuffle=False, drop_last=True, batch_size=batch_size)

    # (Initialize logging)
    experiment = wandb.init(project='U-Net', resume='allow', anonymous='must')
    experiment.config.update(
        dict(epochs=epochs, batch_size=batch_size, learning_rate=learning_rate,
            val_percent=val_percent, save_checkpoint=save_checkpoint)
    )

    logging.info(f'''Starting training:
        Epochs:          {epochs}
        Batch size:      {batch_size}
        Learning rate:   {learning_rate}
        Training size:   {n_train}
        Validation size: {n_val}
        Checkpoints:     {save_checkpoint}
        Device:          {device.type}
    ''')

    # Set up the optimizer and the loss.
    optimizer = optim.Adam(model.parameters())
    criterion = CeDiceLoss(num_classes=label_num)
    global_step = 0
    best_vloss = 100000

    # Training
    for epoch in tqdm(range(1, epochs + 1)):
        
        # Train round
        model.train()
        epoch_loss = 0.0
        for i, batch in enumerate(train_loader):
            images, true_masks = batch[0], batch[1]
            images = images.to(device=device, dtype=torch.float)
            true_masks = true_masks.to(device=device, dtype=torch.long)
            masks_pred = model(images)

            loss = criterion(masks_pred, 
                            F.one_hot(true_masks.squeeze_(1),model.n_classes)
                            .permute(0, 3, 1, 2).float())

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

            global_step += 1
            epoch_loss += loss.item()
            avg_tloss = epoch_loss / (i + 1)
            experiment.log({
                'train loss': loss.item(),
                'train avg loss': avg_tloss,
                'step': global_step,
                'epoch': epoch
            })
        
        # Evaluation round
        model.eval()
        running_vloss = 0.0
        with torch.no_grad():
            for i, vbatch in enumerate(val_loader):
                vinputs, vlabels = vbatch[0], vbatch[1]
                vinputs = vinputs.to(device=device, dtype=torch.float)
                vlabels = vlabels.to(device=device, dtype=torch.long)
                voutputs = model(vinputs)

                vloss = criterion(voutputs, F.one_hot(vlabels.squeeze_(1),model.n_classes).permute(0, 3, 1, 2).float())

                running_vloss += vloss.item()
                avg_vloss = running_vloss / (i + 1)

                if avg_vloss < best_vloss:
                    best_vloss = avg_vloss
                    model_path = cp_path + 'Unet_{}_{}'.format(
                                                    timestamp, global_step)
                    torch.save(model.state_dict(), model_path)


if __name__ == '__main__':
#    args = get_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    model = UNet(n_channels=in_channel, n_classes=label_num)
    model = model.to(device)


    train_model(
        model=model,
        epochs=50,
        batch_size=64,
        device=device,
    )
        
