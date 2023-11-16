"""
This is a boilerplate pipeline 'training'
generated using Kedro 0.18.14
"""


import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks import TQDMProgressBar

from .numpy_datamodule import NumpyDataModule
from .my_model import MyModel


def create_datamodule(data: pd.DataFrame, parameters: dict) -> NumpyDataModule:
    x, y = data.drop("price", axis=1), data["price"]
    return NumpyDataModule(x.to_numpy(), y.to_numpy().flatten())


def create_model(parameters: dict) -> pl.LightningModule:
    return MyModel(**parameters)


def train_model(
    model: pl.LightningModule, dm: pl.LightningDataModule, parameters: dict
) -> pl.LightningModule:
    trainer = pl.Trainer(
        max_epochs=parameters["max_epochs"],
        logger=True,
        callbacks=[TQDMProgressBar()],
        # default_root_dir="data/06_models"
        # strategy="ddp",  # Not on MPS...
    )
    trainer.fit(model, dm)
    return model


def evaluate_model(
    model: pl.LightningModule, dm: pl.LightningDataModule
) -> dict:
    trainer = pl.Trainer(logger=True, callbacks=[TQDMProgressBar()])
    return dict(trainer.validate(model, dm)[0])
