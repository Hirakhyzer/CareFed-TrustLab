from __future__ import annotations

import os
import random

import numpy as np
import torch


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def environment_record() -> dict:
    return {
        "python_hash_seed": os.environ.get("PYTHONHASHSEED"),
        "torch_version": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
    }
