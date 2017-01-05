from symbolic_toolbox.base import SymbolicModel
from symbolic_toolbox.discretizer import GasSymbolicModelBuilder

a = SymbolicModel()
a.add_state_var("x1", 0, 10, 0.5)
a.add_state_var("x1", 0, 8, 0.5)

a.add_control_var("u1", 0, 3, 0.5)

a = GasSymbolicModelBuilder(a, 0.5, len)
a.build()

pass
