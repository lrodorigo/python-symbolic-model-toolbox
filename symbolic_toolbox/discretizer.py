from symbolic_toolbox.base import SymbolicModel


class GasSymbolicModelBuilder(object):

    def __init__(self, symbolic_model, tau, f):
        assert hasattr(f, "__call__")
        assert isinstance(symbolic_model, SymbolicModel)
        self.symbolic_model = symbolic_model
        self.tau = tau
        self.f = f

    def build(self):

        for index_v, v in self.symbolic_model.iterate_over_states_values():
            for index_u, u in self.symbolic_model.iterate_over_control_values():
                #f = lambda t, x: self.f(t, x, u)
                _u = u[0]
                out = [v[0] + v[1]*self.tau + 0.5*_u*self.tau**2, v[1] + _u*self.tau]
                index_out = self.symbolic_model.state_vector_to_symbol(out)

                self.symbolic_model.set_transition(index_v, index_u, index_out)
