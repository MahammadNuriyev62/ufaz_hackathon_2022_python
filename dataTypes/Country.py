from inspect import signature
from random import uniform
import numpy

from scipy.spatial import distance


class Country:
    IMPERIALIST = 1
    COLONY = 2

    def __init__(self, function):
        self.cost = None
        self.model = None
        self.dimension = None
        self.uniqueName = None
        self.function = function
        self.status = Country.COLONY
        self.colonies = []

        # initialize country
        self.init_country()

    def calculate_cost(self):
        self.cost = self.function(*self.model)
        return self.cost

    def init_country(self):
        self.get_dimension()
        self.generate_random_model()

    def generate_random_model(self):
        # self.model = numpy.random.uniform(self.function.lower_bound, self.function.upper_bound, self.dimension)
        self.model = [uniform(self.function.lower_bound, self.function.upper_bound) for _ in range(self.dimension)]
        self.calculate_cost()

    def get_dimension(self):
        if not self.function.dimension:
            sig = signature(self.function.body)
            self.dimension = len(sig.parameters)
        else:
            self.dimension = self.function.dimension

    def __gt__(self, other):
        return self.cost < other.cost

    def __ge__(self, other):
        return self.cost <= other.cost

    def __lt__(self, other):
        return self.cost > other.cost

    def __le__(self, other):
        return self.cost >= other.cost

    def __sub__(self, other):
        return distance.euclidean(self.model, other.model)