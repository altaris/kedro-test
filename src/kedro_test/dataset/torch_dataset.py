"""
Pytorch dataset to handle torch-serializable objects in a kedro-approved way
"""

from pathlib import PurePosixPath
from typing import Any

import fsspec
import torch
from kedro.io import AbstractVersionedDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path


class TorchDataset(AbstractVersionedDataset):
    """
    Kedro dataset implementation for torch-serializable objects. This inclides
    `LightningModule`s. Here's what your catalog entry should look like:

        model:
          type: <project_name>.dataset.TorchDataset
          filepath: data/06_models/model.pt
    """

    def __init__(
        self,
        filepath: PurePosixPath,
        *args,
        **kwargs,
    ):
        super().__init__(filepath, *args, **kwargs)
        protocol, path = get_protocol_and_path(str(self._filepath))
        self._protocol, self._filepath = protocol, PurePosixPath(path)
        _fs_args: dict = {}
        if self._protocol == "file":
            _fs_args.setdefault("auto_mkdir", True)
        self._fs = fsspec.filesystem(self._protocol, **_fs_args)

    def _load(self) -> Any:
        load_path = get_filepath_str(self._get_load_path(), self._protocol)
        with self._fs.open(load_path, mode="rb", encoding="utf-8") as fp:
            return torch.load(fp)  # type: ignore

    def _save(self, data: Any) -> None:
        save_path = get_filepath_str(self._get_save_path(), self._protocol)
        with self._fs.open(save_path, mode="wb", encoding="utf-8") as fp:
            torch.save(data, fp)  # type: ignore

    def _describe(self) -> dict[str, Any]:
        return {
            "filepath": self._filepath,
            "protocol": self._protocol,
            "version": self._version,
        }


TorchDataSet = TorchDataset
