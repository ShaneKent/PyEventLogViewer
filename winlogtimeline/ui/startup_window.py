from tkinter import *
from tkinter.ttk import *
from winlogtimeline import util


class StartupWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Class variables
        self.project_path = None

        # Window parameters
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self._place_widgets()

        self.title('Welcome to PyEventLogViewer!️')

        self.grab_set()

    def _init_widgets(self):
        """
        Creates the elements of this window and sets configuration values.
        :return:
        """
        # Container frame
        self.container = Frame(self)
        # Workspace block
        self.main_container = Frame(self.container)

        self.text = Label(self.main_container)
        self.text.config(text="PyEventLogViewer is a timeline-based tool used to simplify the way\n"
                              "a user can view and explore Windows EVTX files. To begin using this\n"
                              "software you must do the following:\n\n"
                              "\t1) File → New → 'Create a new project'\n"
                              "\t2) Tools → Import Log File → 'Open a specified EVTX file'\n"
                              "\t3) Explore the presented timeline.\n"
                              "\t4) Double-click a specific record to view the XML data for that record.\n"
                              "\t5) File → Export → 'Generate a CSV or HTML file for timeline presentation.'\n\n"
                              "At this point, only System and Security EVTX files are parsable with this software.")

        self.show_var = BooleanVar()
        self.show_check = Checkbutton(self.main_container, text="Don't Show on Startup", variable=self.show_var)

        # Action block
        self.button_ok = Button(self.main_container, text='Ok', underline=0, command=self.callback_close)
        self.bind('<Return>', self.callback_close)
        self.bind('<Escape>', self.callback_close)

        # Focus on window - required for binds to work.
        self.focus_set()

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 15

        # Workspace block
        self.main_container.columnconfigure(0, weight=4)
        self.main_container.grid(row=0, column=0, rowspan=4, columnspan=5, sticky='EW')

        # Information block
        self.text.grid(row=1, column=0, columnspan=5, padx=padding, pady=padding, sticky='NESW')
        self.button_ok.grid(row=4, column=0, padx=padding, pady=padding, sticky='NESW')
        self.show_check.grid(row=4, column=1, padx=padding, pady=padding, sticky='NESW')

        # Specify which portion to auto-expand
        self.container.columnconfigure(0, weight=4)
        self.container.pack(side=LEFT, fill=BOTH)

    def callback_close(self, event=None):
        """
        Callback used to close help window. Destroys the widget and returns control to the master
        without making any changes.
        :return:
        """

        if self.show_var.get():
            self.master.program_config["startup_window"] = False
            util.data.write_config(self.master.program_config)

        self.destroy()
