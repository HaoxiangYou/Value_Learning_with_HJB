from dataclasses import dataclass
import gin
import numpy as np
from typing import Sequence

@gin.configurable
@dataclass
class VHJBControllerConfig:
    # general
    seed: int

    # neural model hyperparameters
    features: Sequence[int]
    normalization_mean: Sequence[float]
    normalization_std: Sequence[float]
    using_batch_norm: bool
    
    # training hyperparameters
    lr: float
    warmup_epochs: int
    epochs: int
    batch_size: int
    regularization: float

    # dataset
    num_of_interior_data: int
    num_of_boundary_data: int
    interior_states_mean: Sequence[float]
    interior_states_std: Sequence[float]
    boundary_states_mean: Sequence[float]
    boundary_states_std: Sequence[float]
    boundary_cost_clip: float

    # trajectories sample hyperparameters
    num_of_trajectories_per_epoch: int
    maximum_step: int
    maximum_buffer_size: int

    # task related hyperparameters
    Q: Sequence[Sequence[float]]
    R: Sequence[Sequence[float]]
    xf: Sequence[float]
    obs_min: Sequence[float]
    obs_max: Sequence[float]

    def __post_init__(self):
        self.normalization_mean = np.array(self.normalization_mean, dtype=np.float32)
        self.normalization_std = np.array(self.normalization_std, dtype=np.float32)
        self.Q = np.array(self.Q, dtype=np.float32)
        self.R = np.array(self.R, dtype=np.float32)
        self.xf = np.array(self.xf, dtype=np.float32)
        self.interior_states_mean = np.array(self.interior_states_mean, dtype=np.float32)
        self.interior_states_std = np.array(self.interior_states_std, dtype=np.float32)
        self.boundary_states_mean = np.array(self.boundary_states_mean, dtype=np.float32)
        self.boundary_states_std = np.array(self.boundary_states_std, dtype=np.float32)
        self.obs_min = np.array(self.obs_min, dtype=np.float32)
        self.obs_max = np.array(self.obs_max, dtype=np.float32)
