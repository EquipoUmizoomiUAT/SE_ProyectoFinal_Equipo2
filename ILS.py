import copy
import random
import ObjectiveFunction, GlobalConfig

rangeMax = 10
rangeMin = -10
maxIterations = 100
config = GlobalConfig.GetGlobalConfig()


def NeighborSolution(solution):
    """
    Creates a neighboring solution by randomly changing the optimal value of one service.
    """
    service = random.choice(list(solution.keys()))  # Choose a random service (temp, humidity, etc.)
    minimum, maximum = config['range']  # Get the range of the chosen service
    newPrediction = random.uniform(minimum, maximum)  # Generate a new random value within the range
    solution['OptValue'] = newPrediction  # Update the optimal value in the solution
    return solution


def CreateSolutionVA(va):
    solution = {
        'RealValue': va,
        'OptValue': random.uniform(config['range'][0], config['range'][1]),
    }
    return solution


def runILS(va):
    initialSolution = CreateSolutionVA(va)
    OB = ObjectiveFunction.ObjectiveFunction()

    sBest = copy.deepcopy(initialSolution)
    vBest = OB.CalculateSatisfaction(initialSolution)

    iterations = 0

    while iterations < maxIterations and vBest != 0:
        newSolution = NeighborSolution(copy.deepcopy(sBest))
        vNewSolution = OB.CalculateSatisfaction(newSolution)
        if vNewSolution < vBest:
            vBest = vNewSolution
            sBest = copy.deepcopy(newSolution)
        iterations += 1

    return sBest['OptValue']
