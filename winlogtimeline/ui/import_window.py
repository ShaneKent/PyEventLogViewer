from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

from winlogtimeline import util
import os


class ImportWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Class variables

        # Window parameters
        self.title('Import Log Files')
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
        self.sv_file = StringVar()
        self.path_container = Frame(self.container)
        self.label_file = Label(self.path_container, text='File:')
        self.entry_file = Entry(self.path_container, width=60, textvariable=self.sv_file)
        self.button_file = Button(self.path_container, width=3, text='...', command=self.callback_path_prompt)

        # Alias block
        self.sv_alias = StringVar()
        self.label_alias = Label(self.container, text='Alias:')
        self.entry_alias = Entry(self.container, textvariable=self.sv_alias)

        # Action block
        self.button_import = Button(self.container, text='Import', underline=0, command=self.callback_import)
        self.button_cancel = Button(self.container, text='Cancel', underline=0, command=self.callback_cancel)
        self.bind('<Alt-i>', self.callback_import)
        self.bind('<Return>', self.callback_import)
        self.bind('<Alt-c>', self.callback_cancel)
        self.bind('<Escape>', self.callback_cancel)

        # Focus on window.
        self.focus_set()

        # Default values
        self.sv_file.set(os.path.join(util.data.get_appdir(), ''))
        self.sv_alias.set('Alias')

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 3

        # Workspace block
        self.label_file.grid(row=0, column=0, padx=padding, sticky='SW')
        self.entry_file.grid(row=1, column=0, columnspan=4, padx=padding, pady=padding, sticky='NESW')
        self.button_file.grid(row=1, column=4, padx=padding, pady=padding, sticky='EW')
        self.path_container.columnconfigure(0, weight=4)
        self.path_container.grid(row=0, column=0, columnspan=5, rowspan=2, sticky='EW')

        # Alias block
        self.label_alias.grid(row=2, column=0, padx=padding, sticky='SW')
        self.entry_alias.grid(row=3, column=0, columnspan=5, padx=padding, pady=padding, sticky='NESW')

        # Action block
        self.button_cancel.grid(row=6, column=3, padx=padding, pady=padding, sticky='EW')
        self.button_import.grid(row=6, column=4, padx=padding, pady=padding, sticky='EW')

        # Specify which column to auto expand
        self.container.columnconfigure(0, weight=4)

        # Place the container frame
        self.container.pack(fill=BOTH)

    def callback_path_prompt(self):
        """
        Callback used to kick off a directory selection prompt.
        :return:
        """
        file = filedialog.askopenfilename(title='Choose an Event Log File',
                                          filetypes=(('Windows Event Log File', '*.evtx'),))
        if len(file) > 0:
            self.sv_file.set(os.path.abspath(file))

    def callback_import(self, event=None):
        """
        Callback used when the import button is pressed. Ensures that the path is valid and performs error handling.
        :return:
        """
        record_file = os.path.abspath(self.sv_file.get())
        if not os.path.isfile(record_file):  # Does the file exist.
            messagebox.showerror('Error', "The file doesn't exists:\n{}".format(record_file))
            return

        aliases = self.master.master.current_project.get_alias_names()
        if self.sv_alias.get() in aliases:
            messagebox.showerror("Error", "The alias name '{}' has already been used.".format(self.sv_alias.get()))
            return

        # call import function here -> calls from the ui.py
        self.master.master.import_function(record_file, self.sv_alias.get())

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
