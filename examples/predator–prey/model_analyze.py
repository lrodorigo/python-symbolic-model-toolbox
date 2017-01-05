from matplotlib import pyplot
from networkx import dijkstra_path

from symbolic_toolbox.base import SymbolicModel
from symbolic_toolbox.trajectories import TrajectoryGenerator

m = SymbolicModel.load_from_file("predator_prey.sm")


def control_sequence_to_state(model, x0, x_destination):
    assert isinstance(model, SymbolicModel)
    x_dest = m.state_vector_to_symbol(x_destination)
    x_source = m.state_vector_to_symbol(x0)
    state_sequence = dijkstra_path(model.transition_graph, x_source, x_dest)
    control_symbols_sequence = []
    _from = x_source

    for state in state_sequence[1:]:
        control_symbols_sequence.append(model.transition_graph[_from][state]['u'])
        _from = state

    return control_symbols_sequence


def limit_cycle_controller(model, _x_limit):
    assert isinstance(model, SymbolicModel)
    x_limit = model.state_vector_to_symbol(_x_limit)

    if x_limit in model.transition_graph[x_limit]:
        return model.transition_graph[x_limit][x_limit]['u']

x_d = [2., 5.]

x0=[2.,2.]
control_symbols_sequence = control_sequence_to_state(m, x0, x_d)
control_symbols_sequence.extend([control_symbols_sequence[-1]]*100)

_, path = TrajectoryGenerator(m, ).trajectory_by_control_symbols(m.state_vector_to_symbol(x0), control_symbols_sequence)

t = range(len(control_symbols_sequence) + 1)

out_x = [p[0] for p in path]
out_y = [p[1] for p in path]
pyplot.figure()
pyplot.plot(t, out_x, t, out_y)
pyplot.figure()
pyplot.step(range(len(control_symbols_sequence)), [m.control_symbol_to_vector(x) for x in control_symbols_sequence])

pyplot.show()