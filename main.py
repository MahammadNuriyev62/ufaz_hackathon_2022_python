from math import cos, exp, pi, sin, sqrt
from dataTypes.Country import Country
from dataTypes.Function import Function
from dataTypes.System import System
from helpers import nested
from helpers.decorators import timer
from visualization import visual


def rosenbrock_function(*args):
    dimension = len(args)
    return sum([100*(args[i + 1] - args[i]**2)**2 + (args[i] - 1)**2 for i in range(dimension - 1)])

def ackley_function(*args):
    dimension = len(args)
    return -20 * exp(-0.2 * sqrt((1/dimension) * sum([arg**2 for arg in args]))) - \
           exp((1/dimension) * sum([cos(2 * pi * arg) for arg in args])) + 20 + exp(1)

def rastrigin_function(*args):  # x and y
    dimension = len(args)
    return 10 * dimension + sum([arg**2 - 10 * cos(2 * pi * arg) for arg in args])

def schwefel_function(*args):  # x and y
    dimension = len(args)
    return 418.9829 * dimension - sum(arg * sin(sqrt(abs(arg))) for arg in args)


rosenbrock = Function(rosenbrock_function, -1, 1, 2)        # minimum --> 0
ackley = Function(ackley_function, -1, 1, 2)                # minimum --> 0
rastrigin = Function(rastrigin_function, -5.12, 5.12, 2)    # minimum --> 0
schwefel = Function(schwefel_function, -500, 500, 2)        # minimum --> 0

POPULATION_SIZE = 100
IMPERIALISTS_SIZE = 10
COLONIES_SIZE = POPULATION_SIZE - IMPERIALISTS_SIZE

functions = (
        ("rosenbrock", rosenbrock),
        ("ackley", ackley),
        ("rastrigin", rastrigin),
        ("schwefel", schwefel)
    )

@timer
def main(name, function):
    print(f"\n\n\n/* <== {name} function ==> */")
    countries = [Country(function) for _ in range(POPULATION_SIZE)]
    system = System(countries, IMPERIALISTS_SIZE)
    print(system.event_loop())
    # nested.find_result(function, 30, POPULATION_SIZE, IMPERIALISTS_SIZE)


if __name__ == '__main__':
    # compute minimum
    for name, function in functions:
        main(name, function)

    # # visualize
    # # comment to disable
    # for name, function in functions:
    #     print(f"\n\n/* <== {name} function ==> */")
    #     countries = [Country(function) for i in range(POPULATION_SIZE)]
    #     system = System(countries, IMPERIALISTS_SIZE)
    #     visual.visualize(system)


