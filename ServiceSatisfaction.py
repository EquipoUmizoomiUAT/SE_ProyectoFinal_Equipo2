class Satisfaction:
    preferences = None
    solution = None

    def __init__(self, config):
        self.preferences = config

    def SetSolution(self, newSolution):
        self.solution = newSolution

    def GetMaxSatisfaction(self):
        vMax = self.preferences['range'][1]
        vMin = self.preferences['range'][0]
        vO = self.solution['OptValue']
        serviceSatisfaction = (vMax - vO) / (vMax - vMin)
        serviceSatisfaction = 1 - serviceSatisfaction
        return round(serviceSatisfaction, 4)

    def GetUserSatisfaction(self, newSolution):
        self.SetSolution(newSolution)
        newSatisfaction = self.GetMaxSatisfaction()
        return newSatisfaction