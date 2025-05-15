import copy


def GetMaxEnergyCost(cost, currentValue, desiredValue):
    totalCost = cost + cost * (desiredValue - currentValue) if currentValue <= desiredValue else 0
    return totalCost


class Energy:
    preferences = None
    solution = None

    def __init__(self, preferences):
        self.preferences = preferences

    def SetSolution(self, newSolution):
        self.solution = copy.deepcopy(newSolution)

    def GetEnergyConsumptionGain(self, newSolution):
        self.SetSolution(newSolution)
        energyGain = 0

        cost = self.preferences['changeCost']
        realValue = self.solution['RealValue']
        desiredValue = self.solution['OptValue']
        minValue = self.preferences['range'][0]
        maxValue = self.preferences['range'][1]

        energyObjective = GetMaxEnergyCost(cost, realValue, desiredValue)
        energyMin = GetMaxEnergyCost(cost, realValue, minValue)
        energyMax = GetMaxEnergyCost(cost, realValue, maxValue)

        try:
            energyConsumption = round(1 - (energyObjective - energyMin) / (energyMax - energyMin), 5)
        except ZeroDivisionError:
            energyConsumption = 0

        energyGain += energyConsumption

        return energyGain