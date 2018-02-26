from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

class FilterWindow(Toplevel):
    def __init__(self, parent, current_project):
        super().__init__(parent)

        # Class variables
        self.current_project = current_project

        # Window parameters
        self.title('Advanced')
        self.resizable(width=True, height=True)

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
        self.work_container = Frame(self.container)

        self.colList = ['- Select Column -']
        self.master.create_colList(self.colList)

        # Column variable
        self.cvar = StringVar(self)
        self.cvar.set(self.colList[0])

        # Filter columns drop down menu
        self.columns = OptionMenu(self.container, self.cvar, *self.colList)
        self.columns.config(width='17')


        self.opList = ['- Select Operation -']

        # Operation variable
        self.ovar = StringVar()
        self.ovar.set(self.opList[0])

        self.operations = OptionMenu(self.container, self.ovar, *self.opList)
        self.operations.config(width='17')

        # User entered filter value variable
        self.val = StringVar()

        # Filter operation value entry field
        self.filterVal = Entry(self.container, textvariable=self.val)
        self.filterVal.config(width='15')

        self.addButton = Button(self.container, text="Add", command=lambda: self.add_filter())

        self.qButton = Button(self.container, text="Query", command=lambda: self.apply_filters())

        self.check_vars = []
        self.checkbuttons = []

        for i, filter in enumerate(self.master.filters):
            label = filter[0] + ' ' + filter[1] + ' ' + filter[2]
            print(label)
            val = filter[3]
            self.check_vars.append(IntVar(value=val))
            self.checkbuttons.append(Checkbutton(self.work_container, text=label,variable=self.check_vars[i]))

        self.cvar.trace_add('write', lambda *args: self.create_opList())

        '''
        self.bind("<Alt-c>", self.destroy)'''

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 3
        i = 1

        self.columns.grid(row=0, column = 0, columnspan=1, sticky='NW')
        self.operations.grid(row=0, column = 1, columnspan=1, sticky='NW')
        self.filterVal.grid(row=0, column = 2, columnspan=1, sticky='NW')
        self.addButton.grid(row=0, column = 3, columnspan=1, sticky='NW')
        self.qButton.grid(row=0, column = 4, columnspan=1, sticky='NW')

        for f in self.checkbuttons:
            print('xzx')
            i+=1


            f.grid(row=i, column=0, columnspan=1, sticky='NWES')


        # Workspace block
        self.work_container.columnconfigure(0, weight=4)
        self.work_container.grid(row=0, column=0, columnspan=5, rowspan=12, sticky='NW')

        #self.container.columnconfigure(0, weight=4)
        self.container.grid(row=0, column=0)


    def create_opList(self):
        inttype = {'Event ID', 'Record Number', 'Recovered', 'Timestamp (UTC)', 'Timestamp'}
        strtype = {'Description', 'Details', 'Event Source', 'Event Log', 'Session ID', 'Account', 'Computer Name',
                   'Source File Alias', 'Record Hash'}
        # This shouldn't be hardcoded. Grab from SQL col type or something.

        column = self.cvar.get()

        self.opList = ['- Select Operation -']
        if column in inttype:
            self.opList = ['=', '<', '>', 'In']
        elif column in strtype:
            self.opList = ['Contains']

        self.operations['menu'].delete(0, 'end')
        for choice in self.opList:
            self.operations['menu'].add_command(label=choice, command=lambda c=choice: self.ovar.set(c))
        self.ovar.set(self.opList[0])

    def add_filter(self):
        padding = 3

        config = [self.cvar.get(), self.ovar.get(), self.filterVal.get(), 1]
        label = ' '.join(config[:3])

        #Disallow empty values
        if config[0] == '- Select Column -' or config[1] == '- Select Operation -':
            return
        if config[2] == '' or config[2] == None:
            print('No value entered!')
            return

        #Disallow duplicate filters
        for f in self.master.filters:
            if f[0] == config[0] and f[1] == config[1] and f[2] == config[2]:
                print('Duplicate filter detected')
                return

        self.master.filters.append(config)

        idx = len(self.check_vars) + 1
        self.check_vars.append(IntVar(value=1))
        self.checkbuttons.append(Checkbutton(self, text=label, variable=self.check_vars[-1]))
        self.checkbuttons[-1].grid(row=idx, column=0, columnspan=1, padx=padding, sticky='NWES')
        return

    def apply_filters(self):

        for i in range(len(self.check_vars)):
            self.master.filters[i][-1] = self.check_vars[i].get()

        self.master.apply_filter()
        self.destroy()