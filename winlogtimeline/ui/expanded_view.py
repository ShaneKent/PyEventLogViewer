from tkinter import *


class ExpandedView(Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.__destroy__)

        self.title('Expanded Record View')
        self.resizable(width=True, height=True)
        self.minsize(width=400, height=300)
        self.maxsize(width=800, height=600)

        self._init_widgets()
        self._pack_widgets()

    def _init_widgets(self):
        self.container = Frame(self, borderwidth=1, relief=SUNKEN)
        self.listbox = Listbox(self.container)

        self.listbox.insert(END, "Double click on a record to view the XML of that record.")

    def _pack_widgets(self):
        self.container.pack(fill=BOTH, expand=1)
        self.listbox.pack(anchor=W, fill=BOTH, expand=1)

    def update_view(self, record):
        """
`       Updates the expanded view record area with the XML for each record.
        :param record: string for the XML that will be displayed.
        :return:
        """
        list = record.split("\n")

        self.listbox.delete(0, END)

        for line in list:
            self.listbox.insert(END, line)

    def __destroy__(self):
        self.master.expanded_view = None
        self.destroy()
