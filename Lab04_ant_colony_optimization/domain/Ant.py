class Ant:
    def __init__(self, initialSensor):
        self.currentSensor = initialSensor
        self.__visitedSensors = [initialSensor]  # each ant adds in the list the starting city (sensor)
        self.localPheromones = dict()
        self.totalPheromone = 0

    def addSensorToVisited(self, sensor):
        self.__visitedSensors.append(sensor)

    @property
    def visitedSensors(self):
        return self.__visitedSensors
