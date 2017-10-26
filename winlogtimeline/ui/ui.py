from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import *

from threading import Thread
from winlogtimeline import util
from winlogtimeline import collector

import os

current_project = None


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.winfo_toplevel().title("PyEventLogViewer")
        self.minsize(width=800, height=600)

        self.menu_bar = MenuBar(self, tearoff=False)
        self.status_bar = StatusBar(self)
        self.toolbar = Toolbar(self)
        self.query_bar = QueryBar(self)
        self.event_section = EventSection(self)

        self.__disable__()
        self.protocol("WM_DELETE_WINDOW", self.__destroy__)

    def __disable__(self):
        self.toolbar.__disable__()
        self.query_bar.__disable__()

    def __enable__(self):
        self.toolbar.__enable__()
        self.query_bar.__enable__()

    def __destroy__(self, *args, **kwargs):
        global current_project

        if current_project is not None:
            answer = messagebox.askyesno("Save Before Close", "Would you like to save the currently opened "
                                                              "project before closing it?")

            if answer:
                current_project.save()
                current_project = None

        self.destroy()


class EventSection(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill=BOTH)


class QueryBar(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=X)

        self.label = Label(self, text="Show Events:", anchor=W, **kwargs)
        self.label.pack(side=LEFT)

        self.variable = StringVar(self)
        self.variable.set("All")

        self.drop_down = OptionMenu(self, self.variable, "System Startup", "System Shutdown", "Time Change",
                                   "All")
        self.drop_down.config(width="15")
        self.drop_down.pack(side=LEFT)

        # -- REMOVE WHEN NOT NEEDED. Only for prototyping reasons.
        self.button = Button(self, text="Query", command=lambda: parent.status_bar.status.config(
            text="Queried for " + self.variable.get() + " events."))
        self.button.pack(side=LEFT)
        # --

    def __disable__(self):
        self.button.config(state=DISABLED)
        self.drop_down.config(state=DISABLED)

    def __enable__(self):
        self.button.config(state=NORMAL)
        self.drop_down.config(state=NORMAL)


class StatusBar(Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.status = Label(parent, text="Notice: Create a new project or open an existing project to get started.",
                            borderwidth=1, relief=SUNKEN, anchor=W, *args,
                            **kwargs)
        self.status.pack(side=BOTTOM, fill=X)


class Toolbar(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, borderwidth=1, relief=SUNKEN, **kwargs)

        self.import_photo = PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'import.gif'))
        self.format_photo = PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'format.gif'))

        self.import_button = Button(self, image=self.import_photo, width="20",
                                    command=lambda: self.import_function())
        self.format_button = Button(self, image=self.format_photo, width="20",
                                    command=lambda: self.format_function())

        self.import_button.pack()
        self.format_button.pack()

        self.pack(side=LEFT, fill=Y)

    def __disable__(self):
        self.import_button.config(state=DISABLED)
        self.format_button.config(state=DISABLED)

    def __enable__(self):
        self.import_button.config(state=NORMAL)
        self.format_button.config(state=NORMAL)

    def import_function(self):
        filename = filedialog.askopenfilename(title="Open a Project File",
                                              filetypes=(("Windows Event Log File", "*.evtx"),))

        if len(filename) == 0:
            return

        filename = os.path.abspath(filename)

        def callback():
            self.master.status_bar.status.config(text="Reading in the Event Log file named System.evtx")
            finish = collector.import_log(filename, "", "")
            self.master.status_bar.status.config(text=finish)

        t = Thread(target=callback)
        t.start()

        return

    def format_function(self):
        self.master.status_bar.status.config(text="'Format' button pressed.")
        return


class MenuBar(Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        parent.config(menu=self)

        self.file_menu = Menu(self, **kwargs)

        self.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="New Project", command=lambda: self.new_project_function())
        self.file_menu.add_command(label="Open Project", command=lambda: self.open_project_function())
        # self.fileMenu.add_command(label="Save Project", command=lambda: self.saveProjectFunction())

    def new_project_function(self):
        global current_project

        if current_project is not None:
            answer = messagebox.askyesno("Save Before Close", "Would you like to save the currently opened "
                                                              "project before closing it?")
            if answer:
                current_project.save()
                current_project = None

        project_path = os.path.join(util.data.get_appdir(), 'Projects', 'New Project')
        current_project = util.project.Project(project_path)
        self.master.status_bar.status.config(text="Project created at " + current_project.get_path())
        self.master.__enable__()

        return

    def open_project_function(self):
        global current_project

        if current_project is not None:
            answer = messagebox.askyesno("Save Before Close", "Would you like to save the currently opened "
                                                              "project before closing it?")

            if answer:
                current_project.save()
                current_project = None

        projects_path = os.path.join(util.data.get_appdir(), 'Projects')
        filename = filedialog.askopenfilename(initialdir=projects_path, title="Open a Project File",
                                              filetypes=(("ELV Project File", "*.elv"),))
        if len(filename) == 0:
            return

        current_project = util.project.Project(filename)
        self.master.status_bar.status.config(text="Project opened at " + current_project.get_path())
        self.master.__enable__()

        return

    def save_project_function(self):
        self.master.status_bar.status.config(text="'Save Project' chosen from menu bar.")
        return
