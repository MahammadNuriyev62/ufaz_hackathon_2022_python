import random as rn
import numpy

from .Country import Country


class Empire:
    def __init__(self, system, imperialist, colonies):
        self.system = system
        self.imperialist: Country = imperialist
        self.colonies: list[Country] = colonies
        self.totalCost = None
        self.threshold = None

        # constants
        self.revolutionRate = 0.3
        self.sigma = 0.1
        self.betta = 1.1

        self.init_empire()

    def init_empire(self):
        self.calculate_total_cost()
        self.calculate_threshold()

    def calculate_total_cost(self):
        self.totalCost = self.imperialist.cost + self.sigma * (self.find_colonies_mean_cost())

    def calculate_threshold(self):
        self.threshold = (self.imperialist.function.upper_bound - self.imperialist.function.lower_bound) / 10

    # UTILISES

    def find_colonies_mean_cost(self):
        coloniesCosts = [country.cost for country in self.colonies]
        length = len(coloniesCosts)
        return 0 if length == 0 else sum(coloniesCosts) / length

    def exchange_imperialist_with(self, colony):
        """
        function that sets a new imperialist for an empire
        :param colony: the colony that will be a new imperialist
        :return: None
        """
        index = self.colonies.index(colony)
        self.colonies[index], self.imperialist = self.imperialist, self.colonies[index]

    def is_near(self):
        """
        function that checks whether self empire has any other empire near to it
        :return: the empire that is near if there is one
        """
        for other in self.system.empires:
            if other != self and abs(other.imperialist - self.imperialist) < self.threshold:
                # empire1, empire2 = self, other
                # return min(empire1, empire2)
                return other

    def check(self, colony: Country):
        """
        utilise function that checks some conditions
        after the model changes in countries
        :param colony: country that changed its model
        :return: None
        """

        # check if there should be new imperialist in current empire
        self.calculate_total_cost()
        if colony > self.imperialist:
            self.exchange_imperialist_with(colony)

        # check if there should be a union of countries
        other = self.is_near()
        if colony.status == Country.IMPERIALIST and other:
            self += other

    def transfer_country_to(self, country, empire):
        """
        function that takes a colony from current empire and
        transfer it to colonies of another empire that won the competition
        :param country: colony that should be transferred
        :param empire: empire to where colony should be transferred
        :return: None
        """
        self.colonies.remove(country)
        empire.colonies.append(country)

    def delete_empire_to(self, empire):
        """
        deletes current empire and transfers its imperialist ot its near empire
        after the unite process
        :param empire: colony of which empire will become imperialist of deleted empire
        :return:  None
        """
        empire.colonies.append(self.imperialist)
        self.system.empires.remove(self)

    # UTILISES

    # OPERATORS

    def __lt__(self, other):
        return self.totalCost > other.totalCost

    def __le__(self, other):
        return self.totalCost >= other.totalCost

    def __gt__(self, other):
        return self.totalCost < other.totalCost

    def __ge__(self, other):
        return self.totalCost <= other.totalCost

    def __add__(self, other):
        return Empire(self.system, self.imperialist, self.colonies + other.colonies)

    # MAIN FUNCTIONS

    def make_assimilation(self):
        for colony in self.colonies:
            colony.model += numpy.random.uniform(0, colony.model * self.betta)
            self.check(colony)

    def make_revolution(self):
        revolutionaries = rn.sample(self.colonies, round(len(self.colonies) * self.revolutionRate))
        for revolutionary in revolutionaries:
            revolutionary.generate_random_model()
            self.check(revolutionary)

    # MAIN FUNCTIONS