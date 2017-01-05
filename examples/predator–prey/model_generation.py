
import pickle
from symbolic_toolbox.base import SymbolicModel
from symbolic_toolbox.discretizer import SampledOdeModelBuilder


A = 1
B = 1
C = 1
D = 1

def f(x, t, u):
    u = u[0]

    dx = [(A-B*x[1])*(x[0] + u),
          (C*x[0]-D)*x[1]]
    return dx


model = SymbolicModel()

model.add_state_var("predators", 0, 20, .2, 0)
model.add_state_var("preies", 0, 20, .2, 0)
model.add_control_var("preies_input", -5, 10, 1, 0)

SampledOdeModelBuilder(model, 0.1, f).build()

model.save("predator_prey.sm")