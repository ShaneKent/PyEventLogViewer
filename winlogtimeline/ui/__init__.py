import tkinter as tk
from winlogtimeline import util


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.winfo_toplevel().title("PyEventLogViewer")
        self.minsize(width=800, height=600)

        self.menubar = Menubar(self)
        self.statusbar = StatusBar(self)
        self.toolbar = Toolbar(self)
        self.querybar = QueryBar(self)
        self.eventsection = EventSection(self)


class EventSection(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        self.frame = tk.Frame(parent, bg="red", *args, **kwargs)
        self.frame.pack(fill=tk.BOTH)

        # -- REMOVE WHEN NOT NEEDED. Only for prototyping reasons.
        # colors = ["red", "blue", "green", "yellow", "orange"]
        colors = ['#DDCEFF', '#FFCECE', '#CEDEF4', '#FFFFC8', '#B5FFC8', '#FFCEFF']

        for i in range(0, 50):
            label = tk.Label(self.frame, text="Event " + str(i), bg=colors[i % 5], anchor=tk.W, *args, **kwargs)
            label.pack(side=tk.TOP, fill=tk.X)
            # --


class QueryBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.querybar = tk.Frame(parent, *args, **kwargs)
        self.querybar.pack(side=tk.TOP, fill=tk.X)

        self.label = tk.Label(self.querybar, text="Show Events:", anchor=tk.W, *args, **kwargs)
        self.label.pack(side=tk.LEFT)

        self.variable = tk.StringVar(self.querybar)
        self.variable.set("All")

        self.dropDown = tk.OptionMenu(self.querybar, self.variable, "System Startup", "System Shutdown", "Time Change",
                                      "All")
        self.dropDown.config(width="15")
        self.dropDown.pack(side=tk.LEFT)

        # -- REMOVE WHEN NOT NEEDED. Only for prototyping reasons.
        self.button = tk.Button(self.querybar, text="Query", command=lambda: parent.statusbar.status.config(
            text="Queried for " + self.variable.get() + " events."))
        self.button.pack(side=tk.LEFT)
        # --


class StatusBar(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        self.status = tk.Label(parent, text="This is a status bar.", bd=1, relief=tk.SUNKEN, anchor=tk.W, *args,
                               **kwargs)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)


class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.toolbar = tk.Frame(parent, bd=1, relief=tk.SUNKEN, *args, **kwargs)

        self.importPhoto = tk.PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'import.gif'))
        self.formatPhoto = tk.PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'format.gif'))

        self.importButton = tk.Button(self.toolbar, image=self.importPhoto, width="20", height="20",
                                      command=lambda: self.importFunction(parent))
        self.formatButton = tk.Button(self.toolbar, image=self.formatPhoto, width="20", height="20",
                                      command=lambda: self.formatFunction(parent))

        self.importButton.pack()
        self.formatButton.pack()

        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)

    def importFunction(self, parent):
        parent.statusbar.status.config(text="'Import' button pressed.")
        return

    def formatFunction(self, parent):
        parent.statusbar.status.config(text="'Format' button pressed.")
        return


class Menubar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.menu = tk.Menu(parent, *args, **kwargs)
        parent.config(menu=self.menu)

        self.fileMenu = tk.Menu(self.menu, *args, **kwargs)

        self.menu.add_cascade(label="File", menu=self.fileMenu)

        self.fileMenu.add_command(label="New Project", command=lambda: self.newProjectFunction(parent))
        self.fileMenu.add_command(label="Open Project", command=lambda: self.openProjectFunction(parent))
        self.fileMenu.add_command(label="Save Project", command=lambda: self.saveProjectFunction(parent))

    def newProjectFunction(self, parent):
        parent.statusbar.status.config(text="'New Project' chosen from menu bar.")
        return

    def openProjectFunction(self, parent):
        parent.statusbar.status.config(text="'Open Project' chosen from menu bar.")
        return

    def saveProjectFunction(self, parent):
        parent.statusbar.status.config(text="'Save Project' chosen from menu bar.")
        return
