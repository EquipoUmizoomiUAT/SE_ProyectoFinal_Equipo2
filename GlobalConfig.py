def GetGlobalConfig():
    config = {
        'range': [20, 30],
        'changeCost': 15
    }
    return config

def GetSatisfactionWeights():
    alpha = 0.5
    beta = 0.5
    return alpha, beta