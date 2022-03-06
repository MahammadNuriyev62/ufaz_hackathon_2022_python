import random as rn

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
        normalizedCosts = []
        for imperialist in imperialists:
            normalizedCost = imperialist.cost - maxCost
            normalizedCosts.append(normalizedCost)

        sumOfNormalizedCost = sum(normalizedCosts)
        powers = []
        for normalizedCost in normalizedCosts:
            power = abs(normalizedCost / sumOfNormalizedCost)
            powers.append(power)

        numberOfColonies = len(self.countries) - imperialists_number
        numbers = []
        for power in powers:
            number = round(power * numberOfColonies)
            numbers.append(number)

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

        normalizedTotalCosts = []
        for empire in self.empires:
            normalizedTotalCost = empire.totalCost + min(self.empires).totalCost  # min empire gives max cost
            normalizedTotalCosts.append(normalizedTotalCost)

        totalNormalizedTotalCosts = sum(normalizedTotalCosts)
        possessionProbabilities = []
        for normalizedTotalCost in normalizedTotalCosts:
            possessionProbability = normalizedTotalCost / totalNormalizedTotalCosts
            possessionProbabilities.append(possessionProbability)

        R = [rn.uniform(0, 1) for _ in possessionProbabilities]
        D = [p - r for p, r in zip(possessionProbabilities, R)]

        if isEmpireEmpty:
            minEmpire.delete_empire_to(minEmpire)
        else:
            minEmpire.transfer_country_to(minCountry, self.empires[D.index(max(D))])

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