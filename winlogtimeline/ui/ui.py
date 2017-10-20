import tkinter.filedialog as filedialog
import tkinter as tk

from threading import Thread
from winlogtimeline import util
from winlogtimeline import collector

currentProject = None


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

        self.__disable__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.__destroy__)

    def __disable__(self, *args, **kwargs):
        self.toolbar.__disable__(self, *args, **kwargs)
        self.querybar.__disable__(self, *args, **kwargs)

    def __destroy__(self, *args, **kwargs):
        global currentProject

        if (currentProject != None):
            SaveBeforeClosing(self)

        self.destroy()


class EventSection(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        self.frame = tk.Frame(parent, *args, **kwargs)
        self.frame.pack(fill=tk.BOTH)


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

    def __disable__(self, parent, *args, **kwargs):
        self.button.config(state=tk.DISABLED)
        self.dropDown.config(state=tk.DISABLED)


class StatusBar(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        self.status = tk.Label(parent, text="Notice: Create a new project or open an existing project to get started.",
                               bd=1, relief=tk.SUNKEN, anchor=tk.W, *args,
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

    def __disable__(self, parent, *args, **kwargs):
        self.importButton.config(state=tk.DISABLED)
        self.formatButton.config(state=tk.DISABLED)

    def importFunction(self, parent):
        def callback():
            parent.statusbar.status.config(text="Reading in the Event Log file.")
            finish = collector.import_log("../tests/System.evtx", "", "")
            parent.statusbar.status.config(text=finish)

        t = Thread(target=callback)
        t.start()

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
        # self.fileMenu.add_command(label="Save Project", command=lambda: self.saveProjectFunction(parent))

    def newProjectFunction(self, parent):
        global currentProject

        if (currentProject != None):
            SaveBeforeClosing(parent)

        currentProject = util.project.Project("./")
        parent.statusbar.status.config(text="Project created at " + currentProject.path)

        return

    def openProjectFunction(self, parent):
        global currentProject

        if (currentProject != None):
            SaveBeforeClosing(parent)

        filename = filedialog.askopenfilename(initialdir="./", title="Open a Project File",
                                              filetypes=(("ELV Project File", "*.elv"),))
        currentProject = util.project.Project(filename)

        parent.statusbar.status.config(text="Project opened at " + currentProject.path)
        return

    def saveProjectFunction(self, parent):
        parent.statusbar.status.config(text="'Save Project' chosen from menu bar.")
        return


class SaveBeforeClosing(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        self.label = tk.Label(self, text="Do you want to save your project before closing it?")
        self.label.pack()

        self.buttonYes = tk.Button(self, text="Yes", command=lambda: self.save())
        self.buttonNo = tk.Button(self, text="No", command=lambda: self.destroy())

        self.buttonYes.pack()
        self.buttonNo.pack()

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def save(self):
        global currentProject

        currentProject.save()
        currentProject = None
        self.destroy()
