import numpy as np
import scipy as sp
from common.controller.controller import Controller
from common.dynamics.linear import LinearDynamics

class LQR(Controller):
    def __init__(self, dynamics:LinearDynamics, Q:np.ndarray, R:np.ndarray) -> None:
        super().__init__()

        assert Q.ndim == 2
        assert R.ndim == 2
        assert Q.shape[0] == Q.shape[1]
        assert R.shape[0] == R.shape[1]
        assert dynamics.A.shape[1] == Q.shape[1]
        assert dynamics.B.shape[1] == R.shape[1]

        self.dynamics = dynamics
        self.Q = Q
        self.R = R

        self.P = sp.linalg.solve_continuous_are(self.dynamics.A, self.dynamics.B, self.Q, self.R)
        self.K = np.dot(sp.linalg.inv(self.R), np.dot(self.dynamics.B.T, self.P))

    def get_control_efforts(self, x):
        return -self.K @ x