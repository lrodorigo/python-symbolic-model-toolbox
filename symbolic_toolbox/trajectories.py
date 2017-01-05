from symbolic_toolbox.base import SymbolicModel


class TrajectoryGenerator(object):
    def __init__(self, symbolic_model):
        assert isinstance(symbolic_model, SymbolicModel)
        self.symbolic_model = symbolic_model

    def trajectory_by_control_values(self, x0, control_sequence):

        out_indexes = []
        out_values = []

        out_values.append(x0)
        x = self.symbolic_model.state_vector_to_symbol(x0)
        out_indexes.append(x)

        for u in control_sequence:
            u_ = self.symbolic_model.control_vector_to_symbol(u)
            x = self.symbolic_model.transitions[x][u_]
            out_indexes.append(x)
            out_values.append(self.symbolic_model.state_symbol_to_vector(x))

        return out_indexes, out_values

    def evolve(self, x0, step_number):

        out_indexes = []
        out_values = []

        out_values.append(x0)
        x = self.symbolic_model.state_vector_to_symbol(x0)
        out_indexes.append(x)
        u0 = self.symbolic_model.control_vector_to_symbol([0. for _ in self.symbolic_model.control_vars])

        for _ in range(step_number):
            x = self.symbolic_model.transitions[x][u0]
            out_indexes.append(x)
            out_values.append(self.symbolic_model.state_symbol_to_vector(x))

        return out_indexes, out_values


    def trajectory_by_control_symbols(self, x0, control_symbols_sequence):
        out_indexes = []
        out_values = []

        out_indexes.append(x0)
        x = x0
        out_values.append(self.symbolic_model.state_symbol_to_vector(x))

        for u in control_symbols_sequence:
            x = self.symbolic_model.transitions[x][u]
            out_indexes.append(x)
            out_values.append(self.symbolic_model.state_symbol_to_vector(x))

        return out_indexes, out_values
