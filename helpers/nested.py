from dataTypes.Country import Country
from dataTypes.System import System
from numpy import std, mean


def find_result(function, iterations, POPULATION_SIZE, IMPERIALISTS_SIZE):
    values = []
    for i in range(iterations):
        countries = [Country(function) for _ in range(POPULATION_SIZE)]
        system = System(countries, IMPERIALISTS_SIZE)
        value = system.event_loop()[0]
        values.append(value)

    print(f"std is --> {std(values)}")
    print(f"mean is --> {mean(values)}")
    print(f"values is --> {values}")
