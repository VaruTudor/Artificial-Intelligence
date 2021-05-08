from gui import *
import matplotlib.pyplot as pl


class UI:
    def __init__(self, newController: controller, newRepository: repository):
        self._controller = newController
        self._repository = newRepository
        self._path = []
        self._stats = []
        self._iterations = []

    @staticmethod
    def _print_menu():
        print("0. Exit")
        print("1. Create random map")
        print("2. Load a map")
        print("3. Save a map")
        print("4. Visualize map")
        print("5. Run the solver")
        print("6. Visualise the statistics")
        print("7. View the drone moving on a path")

    def menu(self):
        while True:
            self._print_menu()
            option = int(input("Read>>"))
            if option == 0:
                break
            if option == 1:
                self._random_map()
            elif option == 2:
                self._load_map()
            elif option == 3:
                self._save_map()
            elif option == 4:
                self._visualize_map()
            elif option == 5:
                self._run_solver()
            elif option == 6:
                self._view_statistics()
            elif option == 7:
                self._view_drone_moving()
            else:
                print("Invalid option")

    def _random_map(self):
        self._repository.map.randomMap()
        self._repository.random_drone()
        print(f"drone initial position is {self._repository.drone}\n")

    def _load_map(self):
        file_name = input("Map file>>")
        if file_name == "":
            self._repository.map.loadMap("test1.map")
        else:
            self._repository.map.loadMap(file_name)
        self._repository.random_drone()

    def _save_map(self):
        file_name = input("Map file>>")
        self._repository.map.saveMap(file_name)

    def _visualize_map(self):
        visualize_map(self._repository)

    def _run_solver(self):
        startTime = time.time()
        self._path, self._stats = self._controller.solver()
        endTime = time.time()
        print(self._stats)
        print("It took seconds")
        print("{:.2f}".format(endTime-startTime))
        print("\n")
        self._view_drone_moving()

    def _view_statistics(self):
        x = []
        average = []
        deviations = []
        for i in range(len(self._stats)):
            x.append(i)
            average.append(self._stats[i][0])
            deviations.append(self._stats[i][1])
        pl.plot(x, average)
        pl.plot(x, deviations)
        pl.show()

    def _view_drone_moving(self):
        print("PATH: ", self._path)
        movingDrone(self._repository.map, self._path, 1)
