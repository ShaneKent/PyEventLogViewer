from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

class FilterWindow(Toplevel):
    def __init__(self, parent, current_project):
        super().__init__(parent)

        # Class variables
        self.current_project = current_project

        # Window parameters
        self.title('Export Timeline')
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self._place_widgets()