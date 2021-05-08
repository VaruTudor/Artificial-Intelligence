# The variables θ, ω, x, v are the four
# (x=position of the cart from the rail origin, v=its velocity)
# state variables to describe the dynamic system, but we use the variables θ and ω(^θ) to control the inverted pendulum
# system.

# θ(theta) corresponds to the angular position (positive is clockwise) of the pendulum
# θ will be x1 and we assume −40° <= x1 <= 40°
THETA = {
    'NVB': (None, -25, -40),
    'NB': (-40, -10),
    'N': (-20, 0),
    'Z': (-5, 5),
    'P': (0, 20),
    'PB': (10, 40),
    'PVB': (25, None, 40)
}

# ω(omega) corresponds to the angular speed
# ω will be x2 and we assume −8 °/s <= x2 <= 8 °/s
# Angular speed is the measure of how fast the central angle of a rotating body changes with respect to time.
# https://www.youtube.com/watch?v=3Lape_vG0Sc
OMEGA = {
    'NB': (None, -3, -8),
    'N': (-6, 0),
    'Z': (-1, 1),
    'P': (0, 6),
    'PB': (3, None, 8)
}

# (PVB) -positive very big
# (PB) - positive big
# (P) - positive
# (Z) - zero
# (N) - negative
# (NB)  - negative big
# (NVB)  negative very big

#     PB      P       Z       N       NB    (x2)
# PVB PVVB    PVVB    PVB     PB      P
# PB  PVVB    PVB     PB      P       Z
# P   PVB     PB      P       Z       N
# Z   PB      P       Z       N       NB
# N   P       Z       N       NB      NVB
# NB  Z       N       NB      NVB     NVVB
# NVB N       NB      NVB     NVVB    NVVB
# (x1)

# rules for the fuzzy system
fuzzyRules = {
    'PVB': {
        'PB': 'PVVB',
        'P': 'PVVB',
        'Z': 'PVB',
        'N': 'PB',
        'NB': 'P'},
    'PB': {
        'PB': 'PVVB',
        'P': 'PVB',
        'Z': 'PB',
        'N': 'P',
        'NB': 'Z'},
    'P': {
        'PB': 'PVB',
        'P': 'PB',
        'Z': 'P',
        'N': 'Z',
        'NB': 'N'},
    'Z': {
        'PB': 'PB',
        'P': 'P',
        'Z': 'Z',
        'N': 'N',
        'NB': 'NB'},
    'N': {
        'NB': 'NVB',
        'N': 'NB',
        'Z': 'N',
        'P': 'Z',
        'PB': 'P'},
    'NB': {
        'PB': 'Z',
        'P': 'N',
        'Z': 'NB',
        'N': 'NVB',
        'NB': 'NVVB'},
    'NVB': {
        'PB': 'N',
        'P': 'NB',
        'Z': 'NVB',
        'N': 'NVVB',
        'NB': 'NVVB'},
}

# To partition the control space as output, we construct nine membership functions for u on its universe which is
# −32 N <= u <= 32 N
vectors = {
    'NVVB': -32,
    'NVB': -24,
    'NB': -16,
    'N': -8,
    'Z': 0,
    'P': 8,
    'PB': 16,
    'PVB': 24,
    'PVVB': 32,
}


class Fuzzifier:
    # using the triangle formula
    def __init__(self, left, right, mean=None):
        self._left = left
        self._right = right
        self._mean = mean
        if self._mean is None:
            self.computeMean()

    def computeMean(self):
        self._mean = (self._left + self._right) / 2

    # 06_KBS_en-p2.pdf page 64
    def computeValueUsingTriangle(self, x):
        if self._left is not None \
                and self._left <= x < self._mean:
            return (x - self._left) / (self._mean - self._left)
        elif self._right is not None \
                and self._mean <= x < self._right:
            return (self._right - x) / (self._right - self._mean)
        else:
            return 0


# gives a fuzzy membership function to a given range
def functions(ranges):
    return {
        fuzzySet: Fuzzifier(*interval)
        for (fuzzySet, interval) in ranges.items()}


# computes the membership for each fuzzy set based on its associated function (values between 0 and 1)
def computeMembership(value, inputFunctions):
    return {
        fuzzySet: function.computeValueUsingTriangle(value)
        for (fuzzySet, function) in inputFunctions.items()}


thetaFunctions = functions(THETA)
omegaFunctions = functions(OMEGA)


def solver(t, w):
    # compute membership degrees for input parameters
    tMembershipValue = computeMembership(t, thetaFunctions)
    wMembershipValue = computeMembership(w, omegaFunctions)

    degreeFTable = {}  # membership degree of F for each set

    for thetaSet in fuzzyRules:
        for omegaSet, f in fuzzyRules[thetaSet].items():
            # Look in the table and for each cell we take the minimum of the membership values of the index set
            value = min(tMembershipValue[thetaSet], wMembershipValue[omegaSet])
            if f not in degreeFTable:
                degreeFTable[f] = value
            else:
                # The membership degree of F to each class will be the maximum value for that class taken from the rules’ table
                degreeFTable[f] = max(value, degreeFTable[f])

    # defuzzify the results for F using a weighted average of the membership degrees and the b values of the sets.
    if sum(degreeFTable.values()) == 0:
        return
    else:
        return sum([degreeFTable[fSet] * vectors[fSet] for fSet in degreeFTable.keys()]) / sum(degreeFTable.values())
