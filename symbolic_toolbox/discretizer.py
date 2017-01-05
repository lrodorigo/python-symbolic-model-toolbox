import numpy as np
import scipy.integrate
import time

from symbolic_toolbox.base import SymbolicModel


class GasSymbolicModelBuilder(object):

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
                start = time.clock()

                result = scipy.integrate.odeint(self.f, v, interval, args=(u, ))
                delta1 += time.clock() - start

                start = time.clock()
                index_out = self.symbolic_model.state_vector_to_symbol(result[1])
                delta2 += time.clock() - start

                start = time.clock()
                self.symbolic_model.set_transition(index_v, index_u, index_out)
                delta3 += time.clock() - start

        pass
