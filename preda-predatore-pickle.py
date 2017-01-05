import math
import pickle

import sys
from matplotlib import pyplot
from pympler import asizeof

from symbolic_toolbox.base import SymbolicModel
from symbolic_toolbox.discretizer import GasSymbolicModelBuilder
from symbolic_toolbox.trajectories import TrajectoryGenerator

a = SymbolicModel()

a.add_state_var("x1", 0, 20, 0.2, 0)
a.add_state_var("x1", 0, 20, 0.2, 0)
a.add_control_var("u1", -5, 10, 1, 0)

A = 1
B = 1
C = 1
D = 1

def f(x, t, u):
    u = u[0]

    dx = [(A-B*x[1])*x[0] + u,
          (C*x[0]-D)*x[1]]
    return dx

GasSymbolicModelBuilder(a, 0.1, f).build()
pickle.dump(a, open("preda-predatore.p", "w"))

"""
print "Dimensione Modello Simbolico: %s kb" % (asizeof.asizeof(a)/1000)

_, path = TrajectoryGenerator(a).get_trajectory([-5.0, 0], [[0.8] for _ in range(100)])

out_x = [p[0] for p in path]
out_y = [p[1] for p in path]

pyplot.plot(out_y, out_x)
pyplot.show()
"""