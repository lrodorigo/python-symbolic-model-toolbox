import numpy as np
import scipy.integrate
import time

from symbolic_toolbox.base import SymbolicModel


class SampledOdeModelBuilder(object):
    """
    This Ode Model Builder builds
    Ordinary Differential Equations symbolic model.
    """

    def __init__(self, symbolic_model, tau, f):
        assert hasattr(f, "__call__")
        assert isinstance(symbolic_model, SymbolicModel)
        self.symbolic_model = symbolic_model
        self.tau = tau
        self.f = f

    def build(self):
        interval = np.array([0, self.tau])
        delta1, delta2, delta3 = 0,0,0
        for index_v, v in self.symbolic_model.iterate_over_states_values():
            for index_u, u in self.symbolic_model.iterate_over_control_values():
                result = scipy.integrate.odeint(self.f, v, interval, args=(u, ))
                index_out = self.symbolic_model.state_vector_to_symbol(result[1])
                self.symbolic_model.set_transition(index_v, index_u, index_out)

