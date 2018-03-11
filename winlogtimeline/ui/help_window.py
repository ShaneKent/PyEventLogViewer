from tkinter import *
from tkinter.ttk import *


class HelpWindow(Toplevel):
    def __init__(self, parent, type):
        super().__init__(parent)

        # Class variables
        self.project_path = None

        # Window parameters
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self._place_widgets()

        if type == "about":
            self.title('About')
            self.text.config(text="The PyEventLogViewer project was developed over the course\n"
                                  "of six months from late 2017 to early 2018 as part of a sponsored\n"
                                  "course at Cal Poly, San Luis Obispo. There were four main\n"
                                  "contributors to this project: Carter Van Deuren, Zach Monroe,\n"
                                  "Sarah Stephens, and Shane Kent. At the time of developing this\n"
                                  "project, all the contributors were studying toward receiving\n"
                                  "their BS in Computer Engineering from Cal Poly, San Luis Obispo.\n\n"
                                  "Version 1.0.0")
            self.repo_link.grid_forget()
            self.email_link.grid_forget()
        elif type == "license":
            self.title('License')

            with open('../LICENSE', 'r') as content_file:
                content = content_file.read()
                self.text.config(text=content)

            self.repo_link.grid_forget()
            self.email_link.grid_forget()
        elif type == "contact":
            self.title("Contact")
            self.text.config(text="If you have any questions, concerns, or issues you can contact\n"
                                  "the developers of this project by emailing the project team\n"
                                  "or by visiting the project repository here:")

            from webbrowser import open_new
            self.repo_link.bind("<Button-1>", lambda callback: open_new(self.repo_link.cget("text")))
            self.email_link.bind("<Button-1>", lambda callback: open_new("mailto:" + self.email_link.cget("text")))

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
        self.repo_link = Label(self.main_container, text="https://github.com/ShaneKent/PyEventLogViewer/",
                               foreground='blue',
                               cursor='hand2', anchor=CENTER)
        self.email_link = Label(self.main_container, text="pyeventlogviewer@gmail.com",
                                foreground='blue', cursor='hand2', anchor=CENTER)

        # Action block
        self.button_ok = Button(self.main_container, text='Ok', underline=0, command=self.destroy)
        self.bind('<Alt-o>', self.callback_close)
        self.bind('<Return>', self.callback_close)
        self.bind('<Escape>', self.callback_close)

        # Focus on window.
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
        self.text.grid(row=1, column=0, padx=padding, pady=padding, sticky='NESW')
        self.repo_link.grid(row=2, column=0, padx=padding, sticky='NEW')
        self.email_link.grid(row=3, column=0, padx=padding, sticky='NEW')
        self.button_ok.grid(row=4, column=0, padx=padding, pady=padding, sticky='NESW')

        # Specify which portion to auto-expand
        self.container.columnconfigure(0, weight=4)
        self.container.pack(side=LEFT, fill=BOTH)

    def callback_close(self, event=None):
        """
        Callback used to close help window. Destroys the widget and returns control to the master
        without making any changes.
        :return:
        """
        self.destroy()
