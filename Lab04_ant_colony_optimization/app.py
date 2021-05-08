from Assignment4.ui import UI
from Assignment4.controller import controller

if __name__ == '__main__':
    myController = controller()
    ui = UI(myController)
    ui.run()
