from typing import Any

import numpy as np
import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader, Dataset, TensorDataset, random_split

DEFAULT_DATALOADER_KWARGS: dict[str, Any] = {
    "batch_size": 265,
    "num_workers": 4,
    "pin_memory": True,
    "persistent_workers": True,
}


class NumpyDataModule(pl.LightningDataModule):
    ds: TensorDataset
    ds_train: Dataset
    ds_test: Dataset

    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        super().__init__()
        self.ds = TensorDataset(
            torch.from_numpy(x).float(),
            torch.from_numpy(y).float(),
        )

    def setup(self, stage: str) -> None:
        if stage in ["test", "predict"]:
            raise ValueError(f"Unsupported stage {stage}")
        self.ds_train, self.ds_test = random_split(self.ds, [0.8, 0.2])

    def train_dataloader(self) -> DataLoader:
        return DataLoader(self.ds_train, **DEFAULT_DATALOADER_KWARGS)

    def val_dataloader(self) -> DataLoader:
        return DataLoader(self.ds_test, **DEFAULT_DATALOADER_KWARGS)
