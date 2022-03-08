import random as rn

import numpy

from .Country import Country
from .Empire import Empire


class System:
    def __init__(self, countries: list, imperialists_number):
        self.countries: list[Country] = countries
        self.empires: list[Empire] = None
        self.init_system(imperialists_number)

    def init_system(self, imperialists_number):
        self.init_imperialists(imperialists_number)

    def get_colonies(self):
        return filter(lambda country: country.status == Country.COLONY, self.countries)

    def get_imperialists(self):
        return filter(lambda country: country.status == Country.IMPERIALIST, self.countries)

    def get_imperialists_except(self, country):
        return filter(lambda c: c.status == Country.IMPERIALIST and c != country, self.countries)

    def get_n_most_powerful(self, number) -> list[Country]:
        return len(self.countries) >= number and tuple(sorted(self.countries, reverse=True))[:number]

    def init_imperialists(self, imperialists_number):
        imperialists = self.get_n_most_powerful(imperialists_number)
        for imperialist in imperialists:
            imperialist.status = Country.IMPERIALIST

        maxCost = min(self.countries).cost
        normalizedCosts = [imperialist.cost - maxCost for imperialist in imperialists]

        sumOfNormalizedCost = sum(normalizedCosts)
        powers = [abs(normalizedCost / sumOfNormalizedCost) for normalizedCost in normalizedCosts]

        numberOfColonies = len(self.countries) - imperialists_number
        numbers = [round(power * numberOfColonies) for power in powers]

        self.distribute_colonies(numbers)

    def distribute_colonies(self, numbers):
        colonies, imperialists, pointer, self.empires =\
            list(self.get_colonies()), self.get_imperialists(), 0, []
        for number, imperialist in zip(numbers, imperialists):
            self.empires.append(Empire(self, imperialist, colonies[pointer:pointer+number]))
            pointer += number

    def competition(self):
        minEmpire: Empire = min(self.empires)
        isEmpireEmpty = len(minEmpire.colonies) == 0
        minCountry = minEmpire.imperialist if isEmpireEmpty else min(minEmpire.colonies)

        maxTotalCost = min(self.empires).totalCost
        normalizedTotalCosts = [empire.totalCost + maxTotalCost for empire in self.empires]

        totalNormalizedTotalCosts = sum(normalizedTotalCosts)
        possessionProbabilities = [normalizedTotalCost / totalNormalizedTotalCosts for normalizedTotalCost in normalizedTotalCosts]

        D = [p - rn.uniform(0, 1) for p in possessionProbabilities]

        empire = self.empires[D.index(max(D))]
        minEmpire.delete_empire_to(empire) if isEmpireEmpty else minEmpire.transfer_country_to(minCountry, empire)

    def event_loop(self):
        """
        MAIN LOOP
        :return: None
        """
        count = 0
        while len(self.empires) > 1:
            for empire in self.empires:
                empire.make_assimilation()
                empire.make_revolution()
            self.competition()
            count += 1
        return self.empires[0].imperialist.calculate_cost(), self.empires[0].imperialist.model