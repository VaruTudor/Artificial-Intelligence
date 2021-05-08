import queue

import pygame

GREEN = (0, 255, 0)


class Service:
    def __init__(self, drone, serviceMap):
        self.__drone = drone
        self.__serviceMap = serviceMap

    def searchAStar(self, finalX, finalY):
        found = False  # conditional flag
        visited = list()
        toVisit = list()
        toVisit.append(tuple((self.__drone.x, self.__drone.y)))
        gCodeDict = dict()  # here we'll store the g values
        gCodeDict[tuple((self.__drone.x, self.__drone.y))] = 0
        node = (-1, -1)  # we initialize with an impossible position to avoid errors
        while toVisit.__len__() != 0 and found is False:
            if toVisit.__len__() == 0:
                return visited
            previous_node = node    # this will be removed from the result
            node = toVisit.pop(0)  # we use it as a queue, so we pop the first element
            visited.append(node)  # mark the next step as visited
            if node[0] == finalX and node[1] == finalY:
                found = True

            neighbors = self.__serviceMap.getValidNeighbors(node[0], node[1])  # here we get all possible moves
            for neighbor in neighbors:
                gCodeDict[neighbor] = gCodeDict[node] + 1  # we add to each new node the g value

            try:
                neighbors.remove(previous_node)     # we don't add the previous node
            except ValueError: continue

            toVisit = neighbors + toVisit
            toVisit = sorted(toVisit,
                             key=lambda element: self.heuristicManhattanDistance(element, (finalX, finalY))
                                                 + gCodeDict[element],
                             reverse=False)  # we sort using the f = g + h

        return visited

    def searchUniformCost(self, finalX, finalY):
        paths = queue.PriorityQueue()
        paths.put((0, [tuple((self.__drone.x, self.__drone.y))]))  # we add a list of nodes (path) with priority 0

        while not paths.empty():
            element = paths.get()  # the path with the smallest priority
            path = element[1]
            current = path[len(path) - 1]  # the last node in the path

            if (finalX, finalY) in path:
                return path  # goal reached

            cost = element[0]
            neighbors = self.__serviceMap.getValidNeighbors(current[0], current[1])  # here we get all possible moves
            for neighbor in neighbors:
                temp = path[:]  # for each neighbor we create an entry in the paths (priority queue)
                temp.append(neighbor)
                paths.put((cost + 1, temp))  # the cost is incremented with 1 (as that is the abstraction for one
                # move in the matrix)

        return list()

    @staticmethod
    def heuristicManhattanDistance(node, goal):
        return abs(node[0]-goal[0]) + abs(node[1]-goal[1])

    def searchGreedy(self, finalX, finalY):
        found = False  # conditional flag
        visited = list()
        toVisit = list()
        toVisit.append(tuple((self.__drone.x, self.__drone.y)))
        while toVisit.__len__() != 0 and found is False:
            if toVisit.__len__() == 0:
                return visited
            node = toVisit.pop(0)  # we use it as a queue, so we pop the first element
            visited.append(node)  # mark the next step as visited
            if node[0] == finalX and node[1] == finalY:
                found = True
            neighbors = self.__serviceMap.getValidNeighbors(node[0], node[1])  # here we get all possible moves
            toVisit = neighbors + toVisit
            toVisit = sorted(toVisit,
                             key=lambda element: self.heuristicManhattanDistance(element, (finalX, finalY)),
                             reverse=False)  # we sort using the heuristic

        return visited

    def getDrone(self):
        return self.__drone

    @staticmethod
    def transform(givenList):
        newList = list()
        for node in givenList:
            newList.insert(0,
                           [node[0], node[1]]
                           )
        return newList

    @staticmethod
    def displayWithPath(image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image
