import math
import pickle
import numpy as np
from symbolic_toolbox.base import SymbolicModel

m = pickle.load(open("predator–prey.p"))
assert isinstance(m, SymbolicModel)
t = range(100)

x_dest = m.state_symbol_to_vector(m.state_vector_to_symbol([5.8, 6.]))
x0 = [2., 2.]
good = False
transitions = m.transitions[m.state_vector_to_symbol(x0)]


for _ in range(5):
    next_ctrl = [0]
    delta_min = np.linalg.norm(x_dest - m.state_symbol_to_vector(transitions[next_ctrl]))
    print "Sono in %s" % transitions[next_ctrl]

    for k, v in transitions.iteritems():
        delta = np.linalg.norm(x_dest - v)
        if delta < delta_min:
            next_ctrl = k
    print "Vado in %s" % transitions[next_ctrl]
    transitions = m.transitions[transitions[next_ctrl]]

"""
out_x = [p[0] for p in path]
out_y = [p[1] for p in path]

pyplot.plot(t, out_x, t, out_y)
pyplot.show()
"""
