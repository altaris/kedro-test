from typing import Any

import pytorch_lightning as pl
import torch
from torch import Tensor, nn


class MyModel(pl.LightningModule):
    model: nn.Module

    def __init__(self, hidden_dim: int = 512) -> None:
        super().__init__()
        self.save_hyperparameters()
        self.model = nn.Sequential(
            nn.Linear(252, hidden_dim),
            nn.SELU(),
            nn.Linear(hidden_dim, 1),
            nn.Flatten(0),
        )

    def _evaluate(self, batch, stage: str | None = None) -> Tensor:
        """Self-explanatory"""
        x, y_true = batch
        y_true = y_true.to(self.device)
        y_pred = self.forward(x)
        loss = nn.functional.mse_loss(y_pred, y_true)
        if stage:
            self.log(f"{stage}/loss", loss, prog_bar=True, sync_dist=True)
        return loss

    def configure_optimizers(self):
        """Override"""
        return torch.optim.Adam(self.parameters())

    # pylint: disable=arguments-differ
    def test_step(self, batch, *_, **__):
        """Override"""
        return self._evaluate(batch, "test")

    # pylint: disable=arguments-differ
    def training_step(self, batch, *_, **__) -> Any:
        """Override"""
        return self._evaluate(batch, "train")

    def validation_step(self, batch, *_, **__):
        """Override"""
        return self._evaluate(batch, "val")

    def forward(self, x: Tensor) -> Tensor:
        return self.model(x.to(self.device))
