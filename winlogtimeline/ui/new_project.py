from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

from winlogtimeline import util
import os


class NewProject(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Class variables
        self.project_path = None

        # Window parameters
        self.title('New Project')
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self._place_widgets()

    def _init_widgets(self):
        """
        Creates the elements of this window and sets configuration values.
        :return:
        """
        # Container frame
        self.container = Frame(self)
        # Workspace block
        self.sv_workspace = StringVar()
        self.sv_workspace.trace('w', lambda *args: self.callback_update_path())
        self.workspace_container = Frame(self.container)
        self.label_workspace = Label(self.workspace_container, text='Workspace:')
        self.entry_workspace = Entry(self.workspace_container, width=60, textvariable=self.sv_workspace)
        self.button_workspace = Button(self.workspace_container, text='...', width=3, command=self.callback_path_prompt)

        # Title block
        self.sv_title = StringVar()
        self.sv_title.trace('w', lambda *args: self.callback_update_path())
        self.label_title = Label(self.container, text='Title:')
        self.entry_title = Entry(self.container, textvariable=self.sv_title)

        # Path block
        self.label_path = Label(self.container, text='The project will be created in the following directory:')
        self.entry_path = Entry(self.container, state='readonly')

        # Action block
        self.button_create = Button(self.container, text='Create', underline=1, command=self.callback_create)
        self.button_cancel = Button(self.container, text='Cancel', underline=0, command=self.callback_cancel)
        self.bind('<Alt-r>', self.callback_create)
        self.bind('<Return>', self.callback_create)
        self.bind('<Alt-c>', self.callback_cancel)
        self.bind('<Escape>', self.callback_cancel)

        # Focus on window.
        self.focus_set()

        # Default values
        self.sv_workspace.set(os.path.join(util.data.get_appdir(), 'Projects'))
        self.sv_title.set('New Project')

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 3

        # Workspace block
        self.label_workspace.grid(row=0, column=0, padx=padding, sticky='SW')
        self.entry_workspace.grid(row=1, column=0, columnspan=4, padx=padding, pady=padding, sticky='NESW')
        self.button_workspace.grid(row=1, column=4, padx=padding, pady=padding, sticky='EW')
        self.workspace_container.columnconfigure(0, weight=4)
        self.workspace_container.grid(row=0, column=0, rowspan=2, columnspan=5, sticky='EW')

        # Title block
        self.label_title.grid(row=2, column=0, padx=padding, sticky='SW')
        self.entry_title.grid(row=3, column=0, columnspan=5, padx=padding, pady=padding, sticky='EW')

        # Path block
        self.label_path.grid(row=4, column=0, padx=padding, sticky='SW')
        self.entry_path.grid(row=5, column=0, columnspan=5, padx=padding, pady=padding, sticky='EW')

        # Action block
        self.button_cancel.grid(row=6, column=3, padx=padding, pady=padding, sticky='EW')
        self.button_create.grid(row=6, column=4, padx=padding, pady=padding, sticky='EW')

        # Specify which portion to auto-expand
        self.container.columnconfigure(0, weight=4)

        # Place the container frame
        self.container.pack(side=LEFT, fill=BOTH)

    def callback_path_prompt(self):
        """
        Callback used to kick off a directory selection prompt.
        :return:
        """
        workspace = filedialog.askdirectory()
        if len(workspace) > 0:
            self.sv_workspace.set(os.path.abspath(workspace))

    def callback_update_path(self):
        """
        Callback used when either the workspace or title entry widgets are modified. Updates the value of the path entry
        widget.
        :return:
        """
        # Update the project path and ensure that the path is valid.
        self.project_path = os.path.join(os.path.abspath(self.sv_workspace.get()), self.sv_title.get())
        # Enable the entry
        self.entry_path.configure(state='normal')
        # Overwrite the current contents
        self.entry_path.delete(0, END)
        self.entry_path.insert(0, self.project_path)
        # Disable the entry
        self.entry_path.configure(state='readonly')

    def callback_create(self, event=None):
        """
        Callback used when the create button is pressed. Ensures that the path is valid and performs error handling.
        :return:
        """
        project_file = os.path.abspath(os.path.join(self.project_path, '{}.elv'.format(self.sv_title.get())))
        if os.path.isfile(project_file):
            messagebox.showerror('Error', 'The project already exists:\n{}'.format(project_file))
            return
        self.master.open_project(project_file)
        if self.master.current_project is None:
            messagebox.showerror('Error', 'An error occurred while attempting to create the project. '
                                          'Please try a different project name or workspace name.')
            return
        self.destroy()

    def callback_cancel(self, event=None):
        """
        Callback used to cancel the project creation process. Destroys the widget and returns control to the master
        without making any changes.
        :return:
        """
        self.destroy()

    def __destroy__(self):
        """
        Returns focus and control to the master.
        :return:
        """
        self.grab_release()
