import numpy as np
import copy

class SymbolicModelVar(object):

    def index_of_value(self, value):
        value = float(value)

        if value < self.min:
            return 0

        index = int((value - self.min) / self.step)
        min_idx = index

        if min_idx < 0:
            return 0

        if min_idx >= len(self._values):
            return len(self._values) - 1

        def _residual(index):
            return abs(self._values[index] - value)
        """
        for i in range(-2, 2):
            tmp_idx = index + i
            if tmp_idx < 0:
                continue

            if tmp_idx >= len(self._values) or min_idx >= len(self._values):
                break

            if _residual(tmp_idx) < _residual(min_idx):
                min_idx = tmp_idx
        """

        return min_idx if min_idx >= 0 else 0

    def _calculate_values(self):
        self._values = np.arange(self.min, self.eq, self.step)
        self._values = np.append(self._values, np.arange(self.eq, self.max, self.step))

    def __init__(self, index, name, min, max, step, eq=0.0):
        self.index = index
        self.step = step
        self.max = max
        self.min = min
        self._range = self.max - self.min
        self.name = name
        self.eq = eq
        self._values = []
        self._calculate_values()

    def __getitem__(self, item):
        if item >= len(self._values):
            return self._values[-1]

        return self._values[item]

    def __len__(self):
        return len(self._values)

    @property
    def values(self):
        return self._values

    def __iter__(self):
        return self._values.__iter__()

class TransictionDict(dict):
    def _hash_vector(self, item):
        assert isinstance(item, list)
        return "".join(str([x for x in item]))

    def __getitem__(self, item):
        return super(TransictionDict, self).__getitem__(self._hash_vector(item))

    def __contains__(self, item):
        return super(TransictionDict, self).__contains__(self._hash_vector(item))

    def __setitem__(self, k, v):
        return super(TransictionDict, self).__setitem__(self._hash_vector(k), v)

class SymbolicModel(object):

    def __init__(self, name=""):
        self.name = name
        self.state_vars = []
        self.control_vars = []
        self.transitions = TransictionDict()

    def add_same_spacing_vars(self, name_array, min, max, step, eq):
        for n in name_array:
            self.add_state_var(n, min, max, step, eq)

    def set_transition(self, start_state_symbol, control_symbol, end_state_symbol,):

        if start_state_symbol not in self.transitions:
            self.transitions[start_state_symbol] = TransictionDict()

        self.transitions[start_state_symbol][control_symbol] = end_state_symbol

    def state_vector_to_symbol(self, vector):
        assert len(vector) == len(self.state_vars), "len(vector) != len(self.state_vars)"
        out = []

        for var_idx, var in enumerate(self.state_vars):
            idx = var.index_of_value(vector[var_idx])
            out.append(idx)

        return out

    def control_vector_to_symbol(self, vector):
        assert len(vector) == len(self.control_vars), "len(vector) != len(self.control_vars)"
        out = []

        for var_idx, var in enumerate(self.control_vars):
            idx = var.index_of_value(vector[var_idx])
            out.append(idx)

        return out

    @property
    def N(self):
        return len(self.state_vars)

    def state_symbol_to_vector(self, symbol):
        comp = [self.state_vars[i][symbol[i]] for i in range(len(self.state_vars))]
        return np.array(comp)

    def control_symbol_to_vector(self, symbol):
        comp = [self.control_vars[i][symbol[i]] for i in range(len(self.control_vars))]
        return np.array(comp)

    def add_state_var(self, name, min, max, step, eq=0.0):
        self.state_vars.append(SymbolicModelVar(len(self.state_vars), name, min, max, step, eq))
        return len(self.state_vars) - 1

    def add_control_var(self, name, min, max, step, eq=0.0):
        self.control_vars.append(SymbolicModelVar(len(self.control_vars), name, min, max, step, eq))
        return len(self.control_vars) - 1

    def iterate_over_control_values(self):
        indexes = [0 for _ in range(len(self.control_vars))]

        def next_index():

            for i, v in enumerate(indexes):
                indexes[i] = (v + 1) % len(self.control_vars[i])

                if indexes[i] > 0:
                    return True

            return False

        go = True

        while go:
            val = self.control_symbol_to_vector(indexes)
            yield indexes, val
            go = next_index()

    def iterate_over_states_values(self):
        indexes = [0 for _ in range(self.N)]

        def next_index():

            for i, v in enumerate(indexes):
                indexes[i] = (v + 1) % len(self.state_vars[i])

                if indexes[i] > 0:
                    return True

            return False

        go = True

        while go:
            old_index = copy.copy(indexes)
            val = self.state_symbol_to_vector(indexes)
            go = next_index()

            yield old_index, val

    @property
    def state_count(self):
        out = 1
        for x in self.state_vars:
            out *= len(x)

        return out


class SymbolicControllerSearch(object):
    def search_control(self, x, u):
        pass

    def is_safe(self, u):
        pass


np.set_printoptions(precision=2)
"""a = SymbolicModel()
a.add_state_var("x1", -3, 2, 1, 0.76)
a.add_state_var("x2", -1, 1, 1, 0.76)
a.add_state_var("x3", -5, 5, 1, 0.76)

print a.state_symbol_to_vector(a.state_vector_to_symbol([-4, 0.22, 3]))
"""
