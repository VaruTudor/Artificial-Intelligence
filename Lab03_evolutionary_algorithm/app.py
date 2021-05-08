from Assignment3.ui import UI
from Assignment3.controller import controller
from Assignment3.repository import repository

if __name__ == '__main__':
    myRepository = repository()
    myController = controller(myRepository)
    ui = UI(myController, myRepository)
    ui.menu()
