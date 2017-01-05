from operator import mul
import pickle
import numpy as np
import copy

from networkx import DiGraph


class SymbolicModelVar(object):

    def index_of_value(self, value):

        if value < self.min:
            return 0

        if value > self._values[-1]:
            return len(self._values) - 1

        index = int((value - self.min) / self.step)
        return index

        """
        min_idx = index

        if min_idx < 0:
            return 0

        if min_idx >= len(self._values):
            return len(self._values) - 1

        def _residual(index):
            return abs(self._values[index] - value)

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

    def to_graph(self):
        out = DiGraph()
        for source, transitions in self.iteritems():
            for u, destination in transitions.iteritems():
                out.add_edge(source, destination, {'u': u})

        return out

class SymbolicModel(object):

    def __init__(self, name=""):
        self.name = name
        self.state_vars = []
        self.control_vars = []
        self.transitions = TransictionDict()
        self._transition_graph = None

    def _build_graph(self):
        self._transition_graph = self.transitions.to_graph()

    @property
    def transition_graph(self):
        if self._transition_graph is None:
            self._build_graph()

        return self._transition_graph

    def add_same_spacing_vars(self, name_array, min, max, step, eq):
        for n in name_array:
            self.add_state_var(n, min, max, step, eq)

    def set_transition(self, start_state_symbol, control_symbol, end_state_symbol,):
        if start_state_symbol not in self.transitions:
            self.transitions[start_state_symbol] = TransictionDict()

        self.transitions[start_state_symbol][control_symbol] = end_state_symbol

    def state_vector_to_symbol(self, vector):
        assert len(vector) == len(self.state_vars), "len(vector) != len(self.state_vars)"
        out = 0
        prod = 1
        v = reversed(self.state_vars)

        for var_idx, var in enumerate(v):
            idx = var.index_of_value(vector[self.N - 1 - var_idx])
            out += idx*prod
            prod *= len(var)

        return out

    def control_vector_to_symbol(self, vector):
        N = len(self.control_vars)
        assert len(vector) == N, "len(vector) != len(self.state_vars)"
        out = 0
        prod = 1
        v = reversed(self.control_vars)

        for var_idx, var in enumerate(v):
            idx = var.index_of_value(vector[N - 1 - var_idx])
            out += idx*prod
            prod *= len(var)

        return out

    @property
    def N(self):
        return len(self.state_vars)

    def state_symbol_to_vector(self, symbol):
        v = reversed(self.state_vars)
        out = np.zeros(self.N)
        prod = 1

        for var_idx, var in enumerate(v):
            prod *= len(var)
            out[self.N - 1 - var_idx] = var[symbol % prod]
            symbol //= prod

        return out

    def control_symbol_to_vector(self, symbol):
        v = reversed(self.control_vars)
        N = len(self.control_vars)
        out = np.zeros(N)
        prod = 1

        for var_idx, var in enumerate(v):
            prod *= len(var)
            out[N - 1 - var_idx] = var[symbol % prod]
            symbol //= prod

        return out

    def save(self, filename):
        bak = self._transition_graph
        pickle.dump(self, open(filename, "w"))
        self._transition_graph = bak

    @staticmethod
    def load_from_file(filename):
        out = pickle.load(open(filename, "r"))
        assert isinstance(out, SymbolicModel)
        return out

    def add_state_var(self, name, min, max, step, eq=0.0):
        self.state_vars.append(SymbolicModelVar(len(self.state_vars), name, min, max, step, eq))
        return len(self.state_vars) - 1

    def add_control_var(self, name, min, max, step, eq=0.0):
        self.control_vars.append(SymbolicModelVar(len(self.control_vars), name, min, max, step, eq))
        return len(self.control_vars) - 1

    def iterate_over_control_values(self):
        for i in range(self.control_count):
            yield i, self.control_symbol_to_vector(i)

    def iterate_over_states_values(self):
        for i in range(self.state_count):
            yield i, self.state_symbol_to_vector(i)

    @property
    def state_count(self):
        out = 1
        for x in self.state_vars:
            out *= len(x)

        return out


    @property
    def control_count(self):
        out = 1
        for x in self.control_vars:
            out *= len(x)

        return out


class SymbolicControllerSearch(object):
    def search_control(self, x, u):
        pass

    def is_safe(self, u):
        pass


np.set_printoptions(precision=2)