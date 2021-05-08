class Sensor:
    def __init__(self, position, visiblePositions):
        self.position = position
        self.visiblePositions = visiblePositions
        self.energy = 0

    def updateEnergy(self, newEnergy):
        self.energy = newEnergy

    def __repr__(self):
        return "Sensor(" + str(self.position) + " sees UP=" \
               + str(self.visiblePositions[0])\
               + ",LEFT=" + str(self.visiblePositions[1]) \
               + ",DOWN=" + str(self.visiblePositions[2]) \
               + ",RIGHT=" + str(self.visiblePositions[3]) + ")"

    def __str__(self):
        return "Sensor(" + str(self.position) + " sees UP=" \
               + str(self.visiblePositions[0]) \
               + ",LEFT=" + str(self.visiblePositions[1]) \
               + ",DOWN=" + str(self.visiblePositions[2]) \
               + ",RIGHT=" + str(self.visiblePositions[3]) + ")"
